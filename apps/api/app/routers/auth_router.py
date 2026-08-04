from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.auth_schema import AccessTokenResponse, LoginRequest, RegisterRequest
from app.schemas.user_schema import UserPublic, UserUpdate
from app.services import auth_service

router = APIRouter()

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_PATH = "/api/v1/auth"


def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.ENV == "production",  # allows plain http on localhost during dev
        samesite="lax",
        max_age=settings.JWT_REFRESH_EXPIRE_DAYS * 24 * 3600,
        path=REFRESH_COOKIE_PATH,
    )


@router.post("/register", response_model=AccessTokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, response: Response, db: Session = Depends(get_db)) -> AccessTokenResponse:
    try:
        user = auth_service.register_user(db, name=payload.name, email=payload.email, password=payload.password)
    except auth_service.EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists"
        ) from exc

    access_token, refresh_token = auth_service.issue_tokens(db, user)
    _set_refresh_cookie(response, refresh_token)
    return AccessTokenResponse(access_token=access_token, user=UserPublic.model_validate(user))


@router.post("/login", response_model=AccessTokenResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> AccessTokenResponse:
    try:
        user = auth_service.authenticate_user(db, email=payload.email, password=payload.password)
    except auth_service.InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        ) from exc

    access_token, refresh_token = auth_service.issue_tokens(db, user)
    _set_refresh_cookie(response, refresh_token)
    return AccessTokenResponse(access_token=access_token, user=UserPublic.model_validate(user))


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)) -> AccessTokenResponse:
    raw_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not raw_refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    try:
        user, access_token, new_refresh_token = auth_service.rotate_refresh_token(db, raw_refresh_token)
    except auth_service.InvalidRefreshTokenError as exc:
        response.delete_cookie(REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token"
        ) from exc

    _set_refresh_cookie(response, new_refresh_token)
    return AccessTokenResponse(access_token=access_token, user=UserPublic.model_validate(user))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response, db: Session = Depends(get_db)) -> None:
    raw_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if raw_refresh_token:
        auth_service.revoke_refresh_token(db, raw_refresh_token)
    response.delete_cookie(REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)


@router.get("/me", response_model=UserPublic)
def get_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)

@router.patch("/me", response_model=UserPublic)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> UserPublic:
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        return UserPublic.model_validate(current_user)
    
    updated_user = auth_service.update_user_profile(db, user=current_user, update_data=update_data)
    return UserPublic.model_validate(updated_user)
