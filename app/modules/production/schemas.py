from pydantic import BaseModel
from datetime import date, time
from typing import Optional

# --- Batch Operator ---
class BatchOperatorCreate(BaseModel):
    operator_name: str
    operator_mob_no: str
    is_active: bool
    user_login_id: int

    class Config:
        from_attributes = True

class BatchOperatorUpdate(BaseModel):
    operator_name: str
    operator_mob_no: str
    is_active: bool
    user_login_id: int

    class Config:
        from_attributes = True

class BatchOperatorResponse(BaseModel):
    id: int
    operator_name: str
    operator_mob_no: str
    is_active: bool
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Clerks ---
class CreateClerk(BaseModel):
    clerk_name: str
    clerk_mob_no: str
    is_active: bool
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateClerk(BaseModel):
    clerk_name: str
    clerk_mob_no: str
    is_active: bool

    class Config:
        from_attributes = True

class ClerkResponse(BaseModel):
    id: int
    clerk_name: str
    clerk_mob_no: str
    is_active: bool
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Batch ---
class CreateBatch(BaseModel):
    batch_name: str
    batch_date: date
    pot_number: int
    stock_item_name: str
    stock_quantity: Optional[int] = 0
    stock_weight: Optional[float] = 0.0
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateBatch(BaseModel):
    batch_name: str
    batch_date: date
    pot_number: int
    stock_item_name: str
    stock_quantity: Optional[int] = 0
    stock_weight: Optional[float] = 0.0
    user_login_id: int

    class Config:
        from_attributes = True

class BatchResponse(BaseModel):
    id: int
    batch_name: str
    batch_date: date
    pot_number: int
    stock_item_name: Optional[str]
    stock_quantity: Optional[int]
    stock_weight: Optional[float]
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Steam On ---
class CreateSteamOn(BaseModel):
    batch_name: str
    steam_on_date: date
    steam_on_time: time
    first_batch_operator: str
    second_batch_operator: str
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateSteamOn(BaseModel):
    batch_name: str
    steam_on_date: date
    steam_on_time: time
    first_batch_operator: str
    second_batch_operator: str
    user_login_id: int

    class Config:
        from_attributes = True

class SteamOnResponse(BaseModel):
    id: int
    batch: BatchResponse
    steam_on_date: date
    steam_on_time: time
    first_batch_operator: BatchOperatorResponse
    second_batch_operator: BatchOperatorResponse
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Steam Off ---
class CreateSteamOff(BaseModel):
    batch_name: str
    steam_off_date: date
    steam_off_time: time
    first_batch_operator: str
    second_batch_operator: str
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateSteamOff(BaseModel):
    batch_name: str
    steam_off_date: date
    steam_off_time: time
    first_batch_operator: str
    second_batch_operator: str
    user_login_id: int

    class Config:
        from_attributes = True

class SteamOffResponse(BaseModel):
    id: int
    batch: BatchResponse
    steam_off_date: date
    steam_off_time: time
    first_batch_operator: BatchOperatorResponse
    second_batch_operator: BatchOperatorResponse
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Drainage ---
class CreateDrainage(BaseModel):
    batch_name: str
    drainage_date: date
    drainage_time: time
    first_batch_operator: str
    second_batch_operator: str
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateDrainage(BaseModel):
    batch_name: str
    drainage_date: date
    drainage_time: time
    first_batch_operator: str
    second_batch_operator: str
    user_login_id: int

    class Config:
        from_attributes = True

class DrainageResponse(BaseModel):
    id: int
    batch: BatchResponse
    drainage_date: date
    drainage_time: time
    first_batch_operator: BatchOperatorResponse
    second_batch_operator: BatchOperatorResponse
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Immerse ---
class CreateImmerse(BaseModel):
    batch_name: str
    immersion_date: date
    immersion_time: time
    first_batch_operator: str
    second_batch_operator: str
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateImmerse(BaseModel):
    batch_name: str
    user_login_id: int
    immersion_date: date
    immersion_time: time
    first_batch_operator: str
    second_batch_operator: str

    class Config:
        from_attributes = True

class ImmerseResponse(BaseModel):
    id: int
    batch: BatchResponse
    immersion_date: date
    immersion_time: time
    first_batch_operator: BatchOperatorResponse
    second_batch_operator: BatchOperatorResponse
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Milling Analysis ---
class CreateMillingAnalysis(BaseModel):
    batch_name: str
    analyzer_clerk_name: str
    milling_rice_moisture_percent: float
    milling_broken_percent: float
    milling_discolor_percent: float
    milling_damaged_percent: float
    milling_output_porridge_30sec: float
    milling_output_final_polisher_30sec: float
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateMillingAnalysis(BaseModel):
    batch_name: str
    analyzer_clerk_name: str
    milling_rice_moisture_percent: float
    milling_broken_percent: float
    milling_discolor_percent: float
    milling_damaged_percent: float
    milling_output_porridge_30sec: float
    milling_output_final_polisher_30sec: float
    user_login_id: int

    class Config:
        from_attributes = True

class MillingAnalysisResponse(BaseModel):
    id: int
    batch: BatchResponse
    analyzer_clerk: ClerkResponse
    milling_rice_moisture_percent: float
    milling_broken_percent: float
    milling_discolor_percent: float
    milling_damaged_percent: float
    milling_output_porridge_30sec: float
    milling_output_final_polisher_30sec: float
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Sorting Analysis ---
class CreateSortingAnalysis(BaseModel):
    batch_name: str
    analyzer_clerk_name: str
    sorted_rice_moisture_percent: float
    sorted_broken_percent: float
    sorted_discolor_percent: float
    sorted_damaged_percent: float
    rejection_rice_percent: float
    sorting_output_30sec: float
    rejection_output_30sec: float
    checker_clerk_name: str
    checking_date: date
    checking_time: time
    verifier_clerk_name: str
    verifying_date: date
    verifying_time: time
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateSortingAnalysis(BaseModel):
    batch_name: str
    analyzer_clerk_name: str
    sorted_rice_moisture_percent: float
    sorted_broken_percent: float
    sorted_discolor_percent: float
    sorted_damaged_percent: float
    rejection_rice_percent: float
    sorting_output_30sec: float
    rejection_output_30sec: float
    checker_clerk_name: str
    checking_date: date
    checking_time: time
    verifier_clerk_name: str
    verifying_date: date
    verifying_time: time
    user_login_id: int

    class Config:
        from_attributes = True

class SortingAnalysisResponse(BaseModel):
    id: int
    batch: BatchResponse
    analyzer_clerk: ClerkResponse
    sorted_rice_moisture_percent: float
    sorted_broken_percent: float
    sorted_discolor_percent: float
    sorted_damaged_percent: float
    rejection_rice_percent: float
    sorting_output_30sec: float
    rejection_output_30sec: float
    checker_clerk: ClerkResponse
    checking_date: date
    checking_time: time
    verifier_clerk: ClerkResponse
    verifying_date: date
    verifying_time: time
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Cross Verification ---
class CreateCrossVerification(BaseModel):
    batch_name: str
    checker_clerk_name: str
    checking_date: date
    checking_time: time
    verifier_clerk_name: str
    verifying_date: date
    verifying_time: time
    paddy_moisture_percent: float
    approver_clerk_name: str
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateCrossVerification(BaseModel):
    batch_name: str
    checker_clerk_name: str
    checking_date: date
    checking_time: time
    verifier_clerk_name: str
    verifying_date: date
    verifying_time: time
    paddy_moisture_percent: float
    approver_clerk_name: str
    user_login_id: int

    class Config:
        from_attributes = True

class CrossVerificationResponse(BaseModel):
    id: int
    batch: BatchResponse
    checker_clerk: ClerkResponse
    checking_date: date
    checking_time: time
    verifier_clerk: ClerkResponse
    verifying_date: date
    verifying_time: time
    paddy_moisture_percent: float
    approver_clerk: ClerkResponse
    user_login: Optional[str]

    class Config:
        from_attributes = True

# --- Lot Details ---
class CreateLot(BaseModel):
    lot_number: int
    lot_moisture_percent: float
    lot_broken_percent: float
    lot_discolor_percent: float
    lot_damaged_percent: float
    lot_lower_grain_percent: float
    lot_chalky_percent: float
    lot_frk_percent: float
    lot_other_percent: float
    checker_clerk: str
    checking_date: date
    checking_time: time
    verifier_clerk: str
    verifying_date: date
    verifying_time: time
    user_login_id: int

    class Config:
        from_attributes = True

class UpdateLot(BaseModel):
    lot_number: int
    lot_moisture_percent: float
    lot_broken_percent: float
    lot_discolor_percent: float
    lot_damaged_percent: float
    lot_lower_grain_percent: float
    lot_chalky_percent: float
    lot_frk_percent: float
    lot_other_percent: float
    checker_clerk_name: str
    checking_date: date
    checking_time: time
    verifier_clerk_name: str
    verifying_date: date
    verifying_time: time

    class Config:
        from_attributes = True

class LotDetailsResponse(BaseModel):
    id: int
    lot_number: int
    lot_moisture_percent: float
    lot_broken_percent: float
    lot_discolor_percent: float
    lot_damaged_percent: float
    lot_lower_grain_percent: float
    lot_chalky_percent: float
    lot_frk_percent: float
    lot_other_percent: float
    checker_clerk_name: Optional[str]
    checking_date: date
    checking_time: time
    verifier_clerk_name: Optional[str]
    verifying_date: date
    verifying_time: time
    user_login: Optional[str]

    class Config:
        from_attributes = True
