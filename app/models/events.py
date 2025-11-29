from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime

# Model for Events
class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(255), index=True)
    date = Column(Date, index=True)

    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow(), server_default=func.now(), onupdate=func.now())

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(255))
    date = Column(Date, default=datetime.utcnow().date())

