from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.db.session import get_db
from app.core.security import security
from app.modules.users.schemas import User as UserSchema
from app.modules.auth.service import auth_service

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

    result = auth_service.login(db, data.user_login_id, data.password)
    
    # Format response to match frontend expectation
    user = result["user"]
    return {
        "user": {
            "id": user.id,
            "user_login_id": user.user_login_id,
            "role": user.user_role,
            "user_first_name": user.user_first_name,
            "user_second_name": user.user_second_name,
        },
        "access_token": result["access_token"],
        "token_type": result["token_type"],
    }

@router.post("/refresh_token")
def refresh_token(
    credentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    result = auth_service.refresh_token(db, token)
    
    user = result["user"]
    return {
        "user": {
            "id": user.id,
            "user_login_id": user.user_login_id,
            "role": user.user_role,
            "user_first_name": user.user_first_name,
            "user_second_name": user.user_second_name
        },
        "access_token": result["access_token"],
        "token_type": result["token_type"]
    }
