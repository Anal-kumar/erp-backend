from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date

from app.db.session import get_db
from app.core.security import get_current_user
import app.models as models
import app.schemas.reminder as schemas

router = APIRouter()

def create_reminder(reminder: schemas.ReminderCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_reminder = models.Reminder(**reminder.model_dump())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.get("/get_reminders", response_model=List[schemas.Reminder])
def get_reminders(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_reminders = db.query(models.Reminder).options(joinedload(models.Reminder.users)).all()
    return db_reminders

@router.get("/get_reminder/{reminder_id}", response_model=schemas.Reminder)
def get_reminder(reminder_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if db_reminder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    return db_reminder

@router.put("/update_reminder/{reminder_id}", response_model=schemas.Reminder)
def update_reminder(reminder_id: int, reminder: schemas.ReminderUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if db_reminder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    
    for key, value in reminder.model_dump().items():
        setattr(db_reminder, key, value)
    
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.delete("/delete_reminder/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_reminder = db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()
    if db_reminder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    db.delete(db_reminder)
    db.commit()
    return {"message": "Reminder deleted successfully"}

# --- License Renewals ---

@router.post("/renewal_doc", response_model=schemas.LicenseRenewal)
def create_renewal(renewal: schemas.LicenseRenewalCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_reminder = db.query(models.Reminder).filter(models.Reminder.id == renewal.reminder_id).first()
    if db_reminder is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")

    db_renewal = models.LicenseRenewal(
        reminder_id=db_reminder.id,
        renewal_date=renewal.renewal_date,
        expiry_date=renewal.expiry_date,
        renewal_amount=renewal.renewal_amount,
        remarks=renewal.remarks,
        user_login_id=renewal.user_login_id
    )

    # Also update expiry date in reminders table
    db_reminder.expiry_date = renewal.expiry_date

    db.add(db_renewal)
    db.commit()
    db.refresh(db_renewal)
    return db_renewal

@router.get("/get_latest_renewal_dates")
def get_latest_renewal_dates(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    rows = db.query(models.LicenseRenewal.renewal_date, models.LicenseRenewal.reminder_id).all()
    return [{"doc_id": r.reminder_id, "renewal_date": r.renewal_date.isoformat() if isinstance(r.renewal_date, date) else r.renewal_date} for r in rows]

@router.get("/get_renewal_history/{reminder_id}")
def get_all_renewal_dates(reminder_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    rows = (
        db.query(
            models.LicenseRenewal.renewal_date,
            models.LicenseRenewal.expiry_date,
            models.LicenseRenewal.renewal_amount,
            models.LicenseRenewal.remarks,
        )
        .filter(models.LicenseRenewal.reminder_id == reminder_id)
        .all()
    )

    if not rows:
        return []

    return [
        {
            "renewal_date": r.renewal_date.isoformat() if isinstance(r.renewal_date, date) else r.renewal_date,
            "expiry_date": r.expiry_date.isoformat() if isinstance(r.expiry_date, date) else r.expiry_date,
            "renewal_amount": r.renewal_amount,
            "remarks": r.remarks,
        }
        for r in rows
    ]
