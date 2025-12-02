from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from app.modules.users.schemas import UserResponse
from app.modules.master_data.schemas import (
    GodownDetails, StockItemsDetails, PackagingDetails
)

# Models for Incoming and Outgoing
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

class StockLedgerDetails(BaseModel):
    id: int
    godown: GodownDetails
    stock_item: StockItemsDetails
    stock_quantity_bags: int
    stock_weight_quintal: float
    last_updated: datetime

    class Config:
        from_attributes = True

# Transaction Stock Item Details Schema
class TransactionStockItemDetails(BaseModel):
    id: int
    transaction_id: int
    stock_items: StockItemsDetails
    number_of_bags: int
    weight: float
    rate: float

    class Config:
        from_attributes = True

# Schema for creating new transaction stock item
class TransactionStockItemCreate(BaseModel):
    # stock_item_id: int
    stock_item_name: str
    number_of_bags: int
    weight: float
    rate: float

    class Config:
        from_attributes = True

# Schema for updating existing transaction stock item
class TransactionStockItemUpdate(BaseModel):
    transaction_id: Optional[int] = None
    stock_item_name: Optional[str] = None
    number_of_bags: Optional[int] = None
    weight: Optional[float] = None
    rate: Optional[float] = None

    class Config:
        from_attributes = True

# Transaction Allowance Details Schema
class AllowanceDeductionDetails(BaseModel):
    id: int
    transaction_id: int
    is_allowance: bool
    allowance_deduction_name: str
    allowance_deduction_amount: int
    remarks: str

    class Config:
        from_attributes = True

# Schema to create new Allowance or Deduction
class AllowanceDeductionCreate(BaseModel):
    is_allowance: bool
    allowance_deduction_name: str
    allowance_deduction_amount: int
    remarks: str


# Schema to update existing transaction deduction
class AllowanceDeductionUpdate(BaseModel):
    transaction_id: Optional[int] = None
    is_allowance: Optional[bool] = None
    allowance_deduction_name: Optional[str] = None
    allowance_deduction_amount: Optional[int] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True

# Transaction Payment Details Schema
class TransactionPaymentDetails(BaseModel):
    id: int
    transaction_id: int
    payment_amount: int
    payment_date: date
    payment_remarks: str

    class Config:
        from_attributes = True

# Schema to create new transaction payment
class TransactionPaymentCreate(BaseModel):
    payment_amount: int
    payment_date: date
    payment_remarks: str

    class Config:
        from_attributes = True

# Schema to update existing transaction payment
class TransactionPaymentUpdate(BaseModel):
    payment_amount: Optional[int] = None
    payment_date: Optional[date] = None
    payment_remarks: Optional[str] = None

    class Config:
        from_attributes = True

# Transaction Packaging Details Schema
class TransactionPackagingDetails(BaseModel):
    id: int
    transaction_id: int
    packaging_id: int
    bag_nos: int
    packaging: PackagingDetails

    class Config:
        from_attributes = True

# Schema for creating transaction packaging
class TransactionPackagingCreate(BaseModel):
    packaging_name: str
    bag_nos: int

    class Config:
        from_attributes = True

# Schema for updating transaction packaging
class TransactionPackagingUpdate(BaseModel):
    transaction_id: Optional[int] = None
    packaging_name: Optional[str] = None
    bag_nos: Optional[int] = None

    class Config:
        from_attributes = True

# Transaction Unloading Point Details Schema
class TransactionUnloadingPointDetails(BaseModel):
    id: int
    transaction_id: int
    godown: GodownDetails
    number_of_bags: int
    remarks: str

    class Config:
        from_attributes = True

# Schema to create new transaction unloading point
class TransactionUnloadingPointCreate(BaseModel):
    godown_id: int
    number_of_bags: int
    remarks: str

    class Config:
        from_attributes = True

# Schema to update existing transaction unloading point
class TransactionUnloadingPointUpdate(BaseModel):
    godown_name: Optional[str] = None
    number_of_bags: Optional[int] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True


# --- Bag Enums ---
class BagsStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"


# --- Response model for bag info ---
class BagDetailsOut(BaseModel):
    id: int
    packaging_name: str
    total_bags: int
    returned_bags: int

class BagReturnRequest(BaseModel):
    packaging_name: str
    returned_count: int
