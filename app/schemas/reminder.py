from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from app.modules.users.schemas import UserResponse

class ReminderBase(BaseModel):
    user_login_id: int
    document_name: str
    document_number: str
    document_detail: str
    issue_date: date
    expiry_date: date
    doc_priority: str
    doc_login_id: str
    doc_login_password: str
    agent_name: str
    agent_address: str
    agent_mob: str
    has_login: bool = False
    remarks: str
    time_stamp: datetime = Field(default_factory=datetime.utcnow)

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    user_login_id: int
    
    class Config:
        from_attributes = True

class LicenseRenewal(BaseModel):
    id: int
    reminder_id: int
    renewal_date: date
    renewal_amount: int
    remarks: str

    users: UserResponse

    class Config:
        from_attributes = True

class LicenseRenewalCreate(BaseModel):
    user_login_id: int
    reminder_id: int
    renewal_date: date
    expiry_date: date
    renewal_amount: int
    remarks: str

    class Config:
        from_attributes = True
