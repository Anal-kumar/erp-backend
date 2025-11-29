from fastapi import APIRouter, HTTPException, Request
from datetime import datetime, date
from typing import Tuple
from pathlib import Path
import hashlib
import string
import json
import app.modules.master_data.schemas as schemas
# I'll check where FirmData schemas are.
# They were likely in schemas.py (monolithic). I should check app/schemas/master_data.py if I moved them there.
# If not, I might need to create app/schemas/firm_details.py.

# I'll assume I need to create app/schemas/firm_details.py because I haven't seen them in master_data.py schemas.
# I'll create the file first.

router = APIRouter()

def decrypt_expiry_date_from_encrypted(encrypted_expiry_date: str) -> str:
    """Decrypt expiry date back to digits."""
    decrypted = ""
    for char in encrypted_expiry_date:
        if "A" <= char <= "Z":
            digit = string.ascii_uppercase.index(char) + 1
            decrypted += str(digit)
        else:
            decrypted += char
    return decrypted

def calculate_checksum(product_name: str, est_id: str, expiry_date: str) -> str:
    data = f"{product_name}|{est_id}|{expiry_date}"
    return hashlib.sha256(data.encode()).hexdigest().upper()[:8]

def verify_serial_key(serial_key: str) -> Tuple[bool, str, str]:
    """Verify full serial string. Returns (valid, message, decrypted_expiry)."""
    parts = serial_key.split("-")
    if len(parts) != 4:
        return False, "Invalid format: expected 4 parts separated by '-'.", None

    product_name, est_id, encrypted_expiry, provided_checksum = parts
    decrypted_expiry = decrypt_expiry_date_from_encrypted(encrypted_expiry)
    calculated_checksum = calculate_checksum(product_name, est_id, decrypted_expiry)

    if calculated_checksum == provided_checksum:
        return True, "Checksum matches. Serial key is valid.", decrypted_expiry
    else:
        return (
            False,
            f"Checksum mismatch. Expected {calculated_checksum} but got {provided_checksum}.",
            decrypted_expiry,
        )
    
def format_expiry_date(expiry_date: str) -> str:
    unformatted_date = datetime.strptime(expiry_date, "%Y%m%d").strftime("%Y-%m-%d")
    formatted_date = datetime.strptime(unformatted_date, "%Y-%m-%d").date()
    return formatted_date

# ------------------- Routes -------------------

@router.get("/get_firm_details")
def get_firm_details():
    project_root = Path(__file__).resolve().parent.parent.parent.parent # app/api/v1/endpoints -> app/api/v1 -> app/api -> app -> root
    # Actually root is where main.py is.
    # app/ is inside ERP-BACKEND/
    # so project_root should be ERP-BACKEND/
    # Path(__file__) is .../app/api/v1/endpoints/firm_details.py
    # .parent = endpoints
    # .parent = v1
    # .parent = api
    # .parent = app
    # .parent = ERP-BACKEND
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    file_path = project_root / "firm_details.json"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="firm_details.json not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="firm_details.json is corrupted")

@router.get("/serial_key_status")
def get_serial_key_status():
    """Check if firm details exist and return serial key status."""
    try:
        project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        file_path = project_root / "firm_details.json"
        
        if not file_path.exists():
            return {
                "exists": False,
                "message": "Firm details not found. Please initialize the database."
            }
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Check if serial key and expiry date exist
        serial_key = data.get("serial_key")
        expires_on = data.get("expires_on")
        
        if not serial_key:
            return {
                "exists": True,
                "valid": False,
                "message": "Serial key not found in firm details."
            }
        
        # Check if expired
        if expires_on:
            try:
                expiry_date = datetime.strptime(expires_on, "%Y-%m-%d").date()
                today = date.today()
                
                if today > expiry_date:
                    return {
                        "exists": True,
                        "valid": False,
                        "expired": True,
                        "expires_on": expires_on,
                        "message": f"License expired on {expires_on}"
                    }
                else:
                    return {
                        "exists": True,
                        "valid": True,
                        "expired": False,
                        "expires_on": expires_on,
                        "message": "License is valid"
                    }
            except Exception as e:
                return {
                    "exists": True,
                    "valid": False,
                    "message": f"Invalid expiry date format: {str(e)}"
                }
        
        return {
            "exists": True,
            "valid": True,
            "message": "Firm details found"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking serial key status: {str(e)}")



# I need schemas for this. I'll comment out the body for now or use dict until I create schemas.
@router.post("/create_firm_details")
async def create_firm_details(payload: dict):
    """Create firm details by verifying serial key and saving to JSON file."""
    try:
        firm_details = payload.get("firm_details", {})
        req = payload.get("req", {})
        serial_key = req.get("serial_key")
        
        if not serial_key:
            raise HTTPException(status_code=400, detail="Serial key is required")
        
        # Verify serial key
        is_valid, message, decrypted_expiry = verify_serial_key(serial_key)
        
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Format expiry date
        try:
            expiry_date = format_expiry_date(decrypted_expiry)
            firm_details["expires_on"] = str(expiry_date)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid expiry date format: {str(e)}")
        
        # Save to JSON file
        project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        file_path = project_root / "firm_details.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(firm_details, f, indent=2, ensure_ascii=False)
        
        return {"message": "Firm details created successfully", "data": firm_details}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating firm details: {str(e)}")

@router.put("/update_firm_details")
async def update_firm_details(payload: dict):
    """Update firm details in JSON file."""
    try:
        firm_details = payload.get("firm_details", {})
        
        # Get existing data
        project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        file_path = project_root / "firm_details.json"
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Firm details not found. Please create first.")
        
        # Read existing data
        with open(file_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        
        # Update with new data
        existing_data.update(firm_details)
        
        # Save updated data
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        return {"message": "Firm details updated successfully", "data": existing_data}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating firm details: {str(e)}")
