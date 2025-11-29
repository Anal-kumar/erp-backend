from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from dateutil import parser

class DayBook(BaseModel):
    id: int
    ie_date: date
    user_login: str
    opening_bal: int = 0
    closing_bal: int = 0
    party_name: Optional[str] = None
    particular: Optional[str] = None
    is_bank: bool = False
    is_receipt: bool = False
    amount: int = 0
    ref_no: str
    remarks: str
    time_stamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('time_stamp', mode='before')
    def parse_time_stamp(cls, v):
        if isinstance(v, str) and v.endswith('Z'):
            return parser.isoparse(v)
        return v

    class Config:
        from_attributes = True
        
class CreateDaybook(BaseModel):
    ie_date: date
    user_login_id: int = None
    party_name: Optional[str] = None
    particular: Optional[str] = None
    is_bank: bool = False
    is_receipt: bool = False
    amount: int = 0
    ref_no: str
    remarks: str
    time_stamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

    @field_validator("ie_date", mode='before')
    def parse_ie_date(cls, value):
        if value in (None, ""):
            return None
        if isinstance(value, date):
            return value
        try:
            return parser.isoparse(str(value)).date()
        except Exception:
            raise ValueError("ie_date must be a valid date in any common format (e.g. 'dd/mm/yyyy', 'yyyy-mm-dd').")

class UpdateDaybook(BaseModel):
    user_login_id: int
    party_name: str
    particular: str
    is_bank: bool
    is_receipt: bool
    amount: int
    ref_no: str
    remarks: str

    class Config:
        from_attributes = True

class DayBookReport(DayBook):
    id: int
    ie_date: date
    user_login_id: int = None
    party_name: Optional[str] = None
    particular: Optional[str] = None
    is_bank: bool = False
    is_receipt: bool = False
    amount: int = 0
    ref_no: str
    remarks: str
