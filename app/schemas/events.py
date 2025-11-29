from pydantic import BaseModel
from datetime import date

class Event(BaseModel):
    id: int
    title: str
    description: str
    date: date

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    description: str
    date: date

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    title: str
    description: str
    date: date

    class Config:
        from_attributes = True

class Announcement(BaseModel):
    id: int
    title: str
    content: str
    date: date

    class Config:
        from_attributes = True

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    date: date

    class Config:
        from_attributes = True

class AnnouncementUpdate(BaseModel):
    title: str
    content: str
    date: date

    class Config:
        from_attributes = True

