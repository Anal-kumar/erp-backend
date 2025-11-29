from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from app.modules.users.schemas import UserResponse

class IncomingOutgoingBase(BaseModel):
    io_date: date
    is_incoming: bool
    rst_bill: str
    brought_by: str
    mob_no: str
    vehicle_no: str
    origin: str
    party_through: str
    transportation_expense: int
    remarks: str
    user_login_id: int

class IncomingOutgoing(IncomingOutgoingBase):
    pass
  
class IncomingOutgoingItemCreate(BaseModel):
    jins: str
    bags_no: int
    quantity: int
    packaging: str
    weight_society: int
    weight_wb: int
    amount: int

    class Config:
        from_attributes = True

class IncomingOutgoingPayments(BaseModel):
    payment_amount: Optional[int] = None
    payment_date: Optional[date] = None

    class Config:
        from_attributes = True

class IncomingOutgoingItem(IncomingOutgoingItemCreate):
    id: int
    incoming_outgoing_id: int

class IncomingOutgoingCreate(IncomingOutgoingBase):
    incoming_outgoing_items: List[IncomingOutgoingItemCreate]
    incoming_outgoing_payment: List[IncomingOutgoingPayments] = []

    class Config:
        from_attributes = True

class IncomingOutgoingUpdate(BaseModel):
    id: int
    io_date: Optional[date] = None
    is_incoming: Optional[bool] = None
    rst_bill: Optional[str] = None
    brought_by: Optional[str] = None
    mob_no: Optional[str] = None
    vehicle_no: Optional[str] = None
    origin: Optional[str] = None
    party_through: Optional[str] = None
    transportation_expense: Optional[int] = None
    remarks: Optional[str] = None
    user_login_id: Optional[int] = None

    incoming_outgoing_items: Optional[List[IncomingOutgoingItemCreate]] = None
    incoming_outgoing_payment: Optional[List[IncomingOutgoingPayments]] = None

    class Config:
        from_attributes = True

class IncomingOutgoingRead(IncomingOutgoingBase):
    id: int
    time_stamp: datetime
    users: UserResponse
    incoming_outgoing_items: List[IncomingOutgoingItem]
    incoming_outgoing_payment: List[IncomingOutgoingPayments] = []

    class Config:
        from_attributes = True
