from datetime import timedelta, datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt, JWTError

from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.modules.users.service import user_service
from app.modules.users.models import User

class AuthService:
    def authenticate(self, db: Session, user_login_id: str, password: str) -> Optional[User]:
        user = user_service.get_by_login_id(db, user_login_id=user_login_id)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def login(self, db: Session, user_login_id: str, password: str) -> dict:
        user = self.authenticate(db, user_login_id, password)
        if not user:
            raise HTTPException(status_code=401, detail="Username or password is incorrect")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.user_login_id,
                "role": user.user_role,
            },
            expires_delta=access_token_expires
        )
        
        return {
            "user": user,
            "access_token": access_token,
            "token_type": "bearer",
        }

    def refresh_token(self, db: Session, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})
            user_login_id: str = payload.get("sub")
            if not user_login_id:
                raise HTTPException(status_code=401, detail="Invalid token payload")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token decode failed")

        user = user_service.get_by_login_id(db, user_login_id=user_login_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Token expiration grace logic
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_time = datetime.utcfromtimestamp(exp_timestamp)
            now = datetime.utcnow()
            if now - exp_time > timedelta(minutes=15):
                raise HTTPException(status_code=401, detail="Token expired too long ago")

        new_token = create_access_token(
            data={"sub": user.user_login_id, "role": user.user_role},
            expires_delta=timedelta(minutes=15)
        )

        return {
            "user": user,
            "access_token": new_token,
            "token_type": "bearer"
        }

auth_service = AuthService()
