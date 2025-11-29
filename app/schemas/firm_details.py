from pydantic import BaseModel, Field
from typing import Optional

class FirmData(BaseModel):
    """Firm data model."""
    product_name: str = Field(..., description="Name of the product")
    est_id: str = Field(..., description="Establishment ID")
    serial_key: str = Field(..., description="Serial key")
    expires_on: Optional[str] = Field("", description="Expiration date")
    api_url: str = Field(..., description="API URL")
    api_port: int = Field(..., description="API port")
    firm_name: str = Field(..., description="Firm name")
    firm_owner_name: str = Field(..., description="Firm owner name")
    firm_short_name: str = Field(..., description="Firm short name")
    firm_address: str = Field(..., description="Firm address")
    firm_mobile_number: str = Field(..., description="Firm mobile number")
    firm_email: str = Field(..., description="Firm email")
    firm_gst_number: str = Field(..., description="Firm GST number")
    firm_pan_number: str = Field(..., description="Firm PAN number")
    page_size: int = Field(..., description="Page size")

    class Config:
        from_attributes = True
        
class FirmDataCreate(FirmData):
    pass

class FirmDataUpdate(FirmData):
    pass

class SerialKeyRequest(BaseModel):
    serial_key: str
