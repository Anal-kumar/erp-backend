from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.security import get_current_user
import app.models.events as models
import app.schemas.events as schemas

router = APIRouter()

@router.get("/get_events", response_model=List[schemas.Event])
def get_events(db: Session = Depends(get_db)):
    events = db.query(models.Events).all()
    return events

@router.get("/get_event/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Events).filter(models.Events.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/create_event", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Events(
        title=event.title,
        description=event.description,
        date=event.date
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/update_event/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db)):
    db_event = db.query(models.Events).filter(models.Events.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_event.title = event.title
    db_event.description = event.description
    db_event.date = event.date
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/delete_event/{event_id}", response_model=schemas.Event)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Events).filter(models.Events.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return db_event

# --- Announcements ---

@router.get("/get_announcements", response_model=List[schemas.Announcement])
def get_announcements(db: Session = Depends(get_db)):
    announcements = db.query(models.Announcement).all()
    return announcements

@router.post("/create_announcement", response_model=schemas.Announcement)
def create_announcement(announcement: schemas.AnnouncementCreate, db: Session = Depends(get_db)):
    db_announcement = models.Announcement(
        title=announcement.title,
        content=announcement.content,
        date=announcement.date
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.put("/update_announcement/{announcement_id}", response_model=schemas.Announcement)
def update_announcement(announcement_id: int, announcement: schemas.AnnouncementUpdate, db: Session = Depends(get_db)):
    db_announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    db_announcement.title = announcement.title
    db_announcement.content = announcement.content
    db_announcement.date = announcement.date
    
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.delete("/delete_announcement/{announcement_id}", response_model=schemas.Announcement)
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    db.delete(db_announcement)
    db.commit()
    return db_announcement

