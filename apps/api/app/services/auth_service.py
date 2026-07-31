from fastapi import HTTPException, status

from app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, RegisterRequest, Token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, data: RegisterRequest) -> dict:
        existing_user = self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_data = {
            "email": data.email,
            "name": data.name,
            "password_hash": get_password_hash(data.password),
        }
        
        user = self.user_repo.create(user_data)
        
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return {
            "user": user,
            "tokens": Token(access_token=access_token, refresh_token=refresh_token)
        }

    def login_user(self, data: LoginRequest) -> dict:
        user = self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return {
            "user": user,
            "tokens": Token(access_token=access_token, refresh_token=refresh_token)
        }
