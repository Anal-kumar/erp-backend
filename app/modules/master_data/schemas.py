from pydantic import BaseModel
from typing import Optional

# Party Details Schema
class PartyDetails(BaseModel):
    id: int
    user_login: str
    party_name: str
    party_mob_no: str
    party_address: str
    party_type: str
    remarks: str

    class Config:
        from_attributes = True

class PartyCreate(BaseModel):
    user_login_id: int
    party_name: str
    party_address: str
    party_mob_no: str
    party_type: str
    remarks: str

    class Config:
        from_attributes = True

class PartyUpdate(BaseModel):
    id: int
    user_login_id: int
    party_name: str
    party_address: str
    party_mob_no: str
    party_type: str
    remarks: str

    class Config:
        from_attributes = True

# Broker Details Schema
class BrokerDetails(BaseModel):
    id: int
    user_login: str
    broker_name: str
    brokerage_rate: float
    broker_mob_no: str
    remarks: str

    class Config:
        from_attributes = True

class BrokerCreate(BaseModel):
    user_login_id: int
    broker_name: str
    brokerage_rate: float
    broker_mob_no: str
    remarks: str

    class Config:
        from_attributes = True

class BrokerUpdate(BaseModel):
    id: int
    user_login_id: int
    broker_name: str
    brokerage_rate: float
    broker_mob_no: str
    remarks: str

    class Config:
        from_attributes = True

# Transportor Details Schema
class TransportorDetails(BaseModel):
    id: int
    user_login: str
    transportor_name: str
    transportor_mob_no: str
    remarks: str

    class Config:
        from_attributes = True

class TransportorCreate(BaseModel):
    user_login_id: int
    transportor_name: str
    transportor_mob_no: str
    remarks: str

    class Config:
        from_attributes = True

class TransportorUpdate(BaseModel):
    id: int
    user_login_id: int
    transportor_name: str
    transportor_mob_no: str
    remarks: str

    class Config:
        from_attributes = True

# Godown Details Schema
class GodownDetails(BaseModel):
    id: int
    user_login: str
    godown_name: str
    godown_qtl_capacity: int
    godown_bags_capacity: int
    remarks: str

    class Config:
        from_attributes = True

class GodownCreate(BaseModel):
    user_login_id: int
    godown_name: str
    godown_qtl_capacity: int
    godown_bags_capacity: int
    remarks: str

    class Config:
        from_attributes = True

class GodownUpdate(BaseModel):
    user_login_id: int
    godown_name: str
    godown_qtl_capacity: int
    godown_bags_capacity: int
    remarks: str

    class Config:
        from_attributes = True

# Stock Items Details Schema
class StockItemsDetails(BaseModel):
    id: int
    user_login: str
    stock_item_name: str
    remarks: str

    class Config:
        from_attributes = True

class StockItemsCreate(BaseModel):
    user_login_id: int
    stock_item_name: str
    remarks: str

    class Config:
        from_attributes = True

class StockItemsUpdate(BaseModel):
    user_login_id: int
    stock_item_name: str
    remarks: str

    class Config:
        from_attributes = True

# Packaging Details Schema
class PackagingDetails(BaseModel):
    id: int
    user_login: str
    packaging_name: str
    bag_weight: int
    packaging_unit: str
    remarks: str

    class Config:
        from_attributes = True

class PackagingCreate(BaseModel):
    user_login_id: int
    packaging_name: str
    bag_weight: int
    packaging_unit: str
    remarks: str

    class Config:
        from_attributes = True

class PackagingUpdate(BaseModel):
    user_login_id: int
    packaging_name: str
    bag_weight: int
    packaging_unit: str
    remarks: str

    class Config:
        from_attributes = True

# Weight Bridge Operator Schema
class WeightBridgeOperator(BaseModel):
    id: int
    user_login: str
    operator_name: str
    operator_mob_no: str
    is_active: bool
    remarks: str

    class Config:
        from_attributes = True

class WeightBridgeOperatorCreate(BaseModel):
    user_login_id: int
    operator_name: str
    operator_mob_no: str
    is_active: bool
    remarks: str

    class Config:
        from_attributes = True

class WeightBridgeOperatorUpdate(BaseModel):
    id: int
    user_login_id: int
    operator_name: str
    operator_mob_no: str
    is_active: bool
    remarks: str

    class Config:
        from_attributes = True

class WeightBridgeOperatorDelete(BaseModel):
    id: int

    class Config:
        from_attributes = True
