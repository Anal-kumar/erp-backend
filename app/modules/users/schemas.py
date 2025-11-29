from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    user_login_id: str
    password: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    user_login_id: str = Field(..., max_length=30)
    user_first_name: str = Field(..., max_length=30)
    user_second_name: str = Field(..., max_length=30)
    mobile_number: str = Field(..., min_length=10, max_length=10)
    designation: str = Field(..., max_length=30)
    user_role: str = Field(..., max_length=30)
    password: str = Field(..., min_length=6, max_length=100)

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    user_first_name: str
    user_second_name: str
    mobile_number: str
    designation: str

    class Config:
        from_attributes = True

class UpdatePassword(BaseModel):
    user_login_id: str = Field(..., max_length=30)
    current_password: str = Field(..., min_length=6, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    user_login_id: str
    user_first_name: str
    user_second_name: str
    mobile_number: str
    designation: str
    user_role: str
    time_stamp: datetime

    class Config:
        from_attributes = True

