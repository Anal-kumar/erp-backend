from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
from app.db.session import get_db
from app.core.security import get_current_user, hash_password, verify_password
from app.modules.users.models import User as UserModel
from app.modules.users.schemas import UserCreate, UserUpdate, UserResponse, UpdatePassword, User as UserSchema

router = APIRouter()

@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    user = current_user["user"]
    return {
        "id": user.id,
        "user_login_id": user.user_login_id,
        "role": user.user_role,
        "user_first_name": user.user_first_name,
        "user_second_name": user.user_second_name,
        "mobile_number": user.mobile_number,
        "designation": user.designation,
    }

@router.get("/get_users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        users = db.query(UserModel).filter(
            UserModel.user_login_id != "superadmin",
            UserModel.user_role != "superadmin"
        ).all()
        return users
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

@router.post("/create_user", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    hashed_pw = hash_password(user.password)
    user_data = user.dict()
    user_data['password'] = hashed_pw
    db_user = UserModel(**user_data)

    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"User with login ID '{user.user_login_id}' already exists",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

@router.get("/get_user/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        user = db.query(UserModel).filter(
            UserModel.id == user_id,
            UserModel.user_login_id != "superadmin",
            UserModel.user_role != "superadmin"
        ).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to fetch user")

@router.put("/update_user/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate data, update failed")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user")

@router.put("/reset_password/{user_id}")
def reset_password(
    user_id: int,
    user: UpdatePassword,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify current password
    if not verify_password(user.current_password, db_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    try:
        db_user.password = hash_password(user.password)
        db.commit()
        db.refresh(db_user)
        return {"detail": "Password updated successfully"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to reset password")

@router.delete("/delete_user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(db_user)
        db.commit()
        return {"detail": "User deleted successfully"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user")
