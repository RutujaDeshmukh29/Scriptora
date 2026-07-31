from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

@router.post("/register", response_model=AuthResponse, status_code=201)
def register(
    data: RegisterRequest, 
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user and return tokens."""
    res = auth_service.register_user(data)
    return AuthResponse(
        user=UserResponse.model_validate(res["user"]),
        tokens=res["tokens"]
    )

@router.post("/login", response_model=AuthResponse)
def login(
    data: LoginRequest, 
    auth_service: AuthService = Depends(get_auth_service)
):
    """Authenticate a user and return tokens."""
    res = auth_service.login_user(data)
    return AuthResponse(
        user=UserResponse.model_validate(res["user"]),
        tokens=res["tokens"]
    )
