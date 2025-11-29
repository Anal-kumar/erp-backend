from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

#  --------------- Labour Operations Schemas ---------------

# Schema for Labour Gang
class LabourGang(BaseModel):
    id: int
    gang_name: str
    gang_mob_no: str
    work_rate: float
    is_active: bool
    remarks: str

    class Config:
        from_attributes = True

# Schema to create Labour Gang
class LabourGangCreate(BaseModel):
    gang_name: str
    gang_mob_no: str
    work_rate: float
    is_active: bool
    remarks: str

    class Config:
        from_attributes = True

# Schema to update Labour Gang
class LabourGangUpdate(BaseModel):
    gang_name: str
    gang_mob_no: str
    work_rate: float
    is_active: bool
    remarks: str

    class Config:
        from_attributes = True

# Schema for Labour Work Items
class LabourWorkItem(BaseModel):
    id: int
    labour_item_name: str
    remarks: str

    class Config:
        from_attributes = True

# Schema to create Labour Work Items
class LabourWorkItemCreate(BaseModel):
    labour_item_name: str
    remarks: str

    class Config:
        from_attributes = True

# Schema to update Labour Work Items
class LabourWorkItemUpdate(BaseModel):
    labour_item_name: str
    remarks: str

    class Config:
        from_attributes = True

# Schema for Labour Work Particulars
class LabourWorkParticulars(BaseModel):
    id: int
    work_name: str
    remarks: str

    class Config:
        from_attributes = True

# Schema to create Labour Work Particulars
class LabourWorkParticularsCreate(BaseModel):
    work_name: str
    remarks: str

    class Config:
        from_attributes = True

# Schema to update Labour Work Particulars
class LabourWorkParticularsUpdate(BaseModel):
    work_name: str
    remarks: str

    class Config:
        from_attributes = True

# Schema for Labour Bag Packaging Weight
class LabourBagPackagingWeight(BaseModel):
    id: int
    bag_weight: int
    remarks: str

    class Config:
        from_attributes = True

# Schema to create Labour Bag Packaging Weight
class LabourBagPackagingWeightCreate(BaseModel):
    bag_weight: int
    remarks: str

    class Config:
        from_attributes = True

# Schema to update Labour Bag Packaging Weight
class LabourBagPackagingWeightUpdate(BaseModel):
    bag_weight: int
    remarks: str

    class Config:
        from_attributes = True

class LabourBagPackagingCreate(LabourBagPackagingWeightCreate):
    bags_nos: int

# Schema for Labour Work Location
class LabourWorkLocation(BaseModel):
    id: int
    work_locations: str
    remarks: str

    class Config:
        from_attributes = True

# Schema to create Labour Work Location
class LabourWorkLocationCreate(BaseModel):
    work_locations: str
    remarks: str

    class Config:
        from_attributes = True

# Schema to update Labour Work Location
class LabourWorkLocationUpdate(BaseModel):
    work_locations: str
    remarks: str

    class Config:
        from_attributes = True

# ------------------ Labour Operations Schemas End -------------------

# ------------------ Voucher Update Schemas -------------------

# Schema to update Labour Gang
class VoucherGangUpdate(BaseModel):
    gang_id: int             # FK to LabourGang
    work_rate: float

    class Config:
        from_attributes = True

# Schema to update Labour Work Items
class VoucherWorkItemUpdate(BaseModel):
    work_item_id: int        # FK to LabourWorkItem

    class Config:
        from_attributes = True

# Schema to update Labour Work Particulars
class VoucherParticularUpdate(BaseModel):
    particulars_id: int      # FK to LabourWorkParticulars

    class Config:
        from_attributes = True

# Schema to update Labour Bag Packaging
class VoucherBagPackagingUpdate(BaseModel):
    bag_packaging_id: int    # FK to LabourBagPackagingWeight
    bags_nos: int
    gang_id: int

    class Config:
        from_attributes = True

# Schema to update Labour Work Location
class VoucherLocationUpdate(BaseModel):
    labour_work_location_id_origin: int
    labour_work_location_id_destination: int

    class Config:
        from_attributes = True

# ------------------ Voucher Update Schemas End -------------------

# ------------------ Voucher Response Schemas -------------------

# Schema for Labour Gang response
class VoucherGang(BaseModel):
    id: int
    work_rate: float
    gang: LabourGang   # nested master

    class Config:
        from_attributes = True

# Schema for Labour Work Item response
class VoucherWorkItem(BaseModel):
    id: int
    work_item: LabourWorkItem   # nested master

    class Config:
        from_attributes = True

# Schema for Labour Work Particulars response
class VoucherParticular(BaseModel):
    id: int
    particular: LabourWorkParticulars   # nested master

    class Config:
        from_attributes = True

# Schema for Labour Bag Packaging response
class VoucherBagPackaging(BaseModel):
    id: int
    bags_nos: int
    bag_packaging: LabourBagPackagingWeight # nested master
    gang: Optional[LabourGang]

    class Config:
        from_attributes = True

# Schema for Labour Work Location response
class VoucherLocation(BaseModel):
    id: int
    location_origin: LabourWorkLocation # nested master
    location_destination: LabourWorkLocation    # nested master

    class Config:
        from_attributes = True


# ------------------ Response Schemas End -------------------

# ------------------ Helper Classes to create Labour Payment Vouchers ------------------

# schema for labour gang
class VoucherGangCreate(BaseModel):
    gang_name: str
    work_rate: float
    remarks: str

    class Config:
        from_attributes = True

# schema for labour work items
class VoucherWorkItemsCreate(BaseModel):
    work_item_name: str
    remarks: str

    class Config:
        from_attributes = True

# schema for labour work particulars
class VoucherWorkParticularsCreate(BaseModel):
    particular_name: str
    remarks: str

    class Config:
        from_attributes = True

# schema for labour bag packaging
class VoucherBagPackagingCreate(BaseModel):
    bag_weight: int
    bags_nos: int
    gang_name: str
    remarks: str

    class Config:
        from_attributes = True

# schema for labour work locations
class VoucherLocationCreate(BaseModel):
    work_locations: str
    remarks: str

    class Config:
        from_attributes = True

# ------------------- Helper Classes End -------------------

# ------------------ Main Model: LabourPaymentVouchers ------------------

# Schema to create Labour Payment Voucher
class LabourPaymentVoucherCreate(BaseModel):
    vch_date: date
    remarks: str
    user_login_id: int

    labour_gang: List[VoucherGangCreate] = []
    labour_work_item: List[VoucherWorkItemsCreate] = []
    labour_work_particulars: List[VoucherWorkParticularsCreate] = []
    labour_bag_packaging_weight: List[VoucherBagPackagingCreate] = []
    labour_work_location_id_origin: List[VoucherLocationCreate] = []
    labour_work_location_id_destination: List[VoucherLocationCreate] = []

    class Config:
        from_attributes = True

# Schema to update Labour Payment Voucher
class LabourPaymentVoucherUpdate(BaseModel):
    vch_date: date
    remarks: str
    user_login_id: int

    voucher_gangs: List[VoucherGangUpdate] = []
    voucher_work_items: List[VoucherWorkItemUpdate] = []
    voucher_particulars: List[VoucherParticularUpdate] = []
    voucher_bag_packagings: List[VoucherBagPackagingUpdate] = []
    voucher_locations: List[VoucherLocationUpdate] = []

    class Config:
        from_attributes = True

# Schema for Labour Payment Vouchers response
class LabourPaymentVoucher(BaseModel):
    id: int
    vch_date: date
    remarks: str
    user_login: Optional[str]
    time_stamp: datetime

    voucher_gangs: List[VoucherGang] = []
    voucher_work_items: List[VoucherWorkItem] = []
    voucher_particulars: List[VoucherParticular] = []
    voucher_bag_packagings: List[VoucherBagPackaging] = []
    voucher_locations: List[VoucherLocation] = []

    class Config:
        from_attributes = True

# ------------------ Main Model: LabourPaymentVouchers End -------------------
