from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum
from app.modules.master_data.schemas import StockItemsDetails, PackagingDetails, GodownDetails

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

class TransactionStockItemCreate(BaseModel):
    # stock_item_id: int
    stock_item_name: str
    number_of_bags: int
    weight: float
    rate: float

    class Config:
        from_attributes = True

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

class AllowanceDeductionCreate(BaseModel):
    is_allowance: bool
    allowance_deduction_name: str
    allowance_deduction_amount: int
    remarks: str

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

class TransactionPaymentCreate(BaseModel):
    payment_amount: int
    payment_date: date
    payment_remarks: str

    class Config:
        from_attributes = True

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

class TransactionPackagingCreate(BaseModel):
    packaging_name: str
    bag_nos: int

    class Config:
        from_attributes = True

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

class TransactionUnloadingPointCreate(BaseModel):
    godown_id: int
    number_of_bags: int
    remarks: str

    class Config:
        from_attributes = True

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

from app.modules.users.schemas import UserResponse
from typing import List
from datetime import datetime

class BagReturnRequest(BaseModel):
    packaging_name: str
    returned_count: int

class TransactionMillOperationsBase(BaseModel):
    rst_number: Optional[str] = None
    bill_number: Optional[str] = None
    transaction_date: Optional[date] = None
    transaction_type: Optional[bool] = None
    party_name: Optional[str] = None
    broker_name: Optional[str] = None
    transportor_name: Optional[str] = None
    gross_weight: Optional[int] = None
    tare_weight: Optional[int] = None
    operator_name: Optional[str] = None
    vehicle_number: Optional[str] = None
    remarks: Optional[str] = None

class TransactionMillOperationsCreate(TransactionMillOperationsBase):
    rst_number: str
    bill_number: str
    transaction_date: date
    transaction_type: bool
    party_name: str
    broker_name: str
    transportor_name: str
    gross_weight: int
    tare_weight: int
    operator_name: str
    vehicle_number: str
    user_login_id: int
    
    transaction_stock_items: List[TransactionStockItemCreate]
    payments: List[TransactionPaymentCreate]
    packagings: List[TransactionPackagingCreate]
    unloadings: List[TransactionUnloadingPointCreate]
    allowances_deductions: List[AllowanceDeductionCreate]

class TransactionMillOperationsUpdate(TransactionMillOperationsBase):
    transaction_stock_items: Optional[List[TransactionStockItemCreate]] = None
    payments: Optional[List[TransactionPaymentCreate]] = None
    packagings: Optional[List[TransactionPackagingCreate]] = None
    unloadings: Optional[List[TransactionUnloadingPointCreate]] = None
    allowances_deductions: Optional[List[AllowanceDeductionCreate]] = None

class TransactionMillOperations(TransactionMillOperationsBase):
    id: int
    user_login_id: int
    time_stamp: Optional[datetime] = None
    
    transaction_stock_items: List[TransactionStockItemDetails] = []
    transaction_payments_mill_operations: List[TransactionPaymentDetails] = []
    transaction_packaging_details: List[TransactionPackagingDetails] = []
    transaction_unloading_point_details: List[TransactionUnloadingPointDetails] = []
    transaction_allowance_deduction_details: List[AllowanceDeductionDetails] = []
    bag_details: List[BagDetailsOut] = []
    
    users: Optional[UserResponse] = None

    class Config:
        from_attributes = True
