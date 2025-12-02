from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from datetime import timedelta, datetime
from app.db.session import get_db
from app.core.config import settings
from app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    security
)
from app.modules.users.schemas import User as UserSchema
from app.modules.users.models import User as UserModel
from jose import jwt, JWTError

router = APIRouter()

@router.post("/login")
def login(data: UserSchema, db: Session = Depends(get_db)):
    # Check if the database is initialized (has "users" table)
    inspector = inspect(db.bind)
    if "users" not in inspector.get_table_names():
        raise HTTPException(
            status_code=500,
            detail="Database is not initialized. Please run migrations first."
        )

    user = authenticate_user(db, data.user_login_id, data.password)
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
        "user": {
            "id": user.id,
            "user_login_id": user.user_login_id,
            "role": user.user_role,
            "user_first_name": user.user_first_name,
            "user_second_name": user.user_second_name,
        },
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/refresh_token")
def refresh_token(
    credentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})
        user_login_id: str = payload.get("sub")
        if not user_login_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token decode failed")

    # Always get fresh user role from DB
    user = db.query(UserModel).filter(UserModel.user_login_id == user_login_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Token expiration grace logic (optional)
    exp_timestamp = payload.get("exp")
    if exp_timestamp:
        exp_time = datetime.utcfromtimestamp(exp_timestamp)
        now = datetime.utcnow()
        if now - exp_time > timedelta(minutes=15):
            raise HTTPException(status_code=401, detail="Token expired too long ago")

    # Build new token using real user role from DB
    new_token = create_access_token(
        data={"sub": user.user_login_id, "role": user.user_role},
        expires_delta=timedelta(minutes=15)
    )

    return {
        "user": {
            "id": user.id,
            "user_login_id": user.user_login_id,
            "role": user.user_role,
            "user_first_name": user.user_first_name,
            "user_second_name": user.user_second_name
        },
        "access_token": new_token,
        "token_type": "bearer"
    }
