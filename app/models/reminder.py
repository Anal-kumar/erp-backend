from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    document_name = Column(String(50), index=True)
    document_number = Column(String(30), index=True)
    document_detail = Column(String(50), index=True)
    issue_date = Column(Date, index=True)
    expiry_date = Column(Date, index=True)
    doc_priority = Column(String, index=True)
    doc_login_id = Column(String(30), index=True)
    doc_login_password = Column(String(30), index=True)
    agent_name = Column(String(50), index=True)
    agent_address = Column(String(100), index=True)
    agent_mob = Column(String(10), index=True)
    has_login = Column(Boolean, default=False)
    remarks = Column(String(50), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow(), server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="reminders")
    license_renewal = relationship("LicenseRenewal", back_populates="reminders")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class LicenseRenewal(Base):
    __tablename__ = "license_renewal"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    reminder_id = Column(Integer, ForeignKey("reminders.id"), index=True)
    renewal_date = Column(Date, index=True)
    expiry_date = Column(Date, index=True)
    renewal_amount = Column(Integer, index=True)
    remarks = Column(String(50), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow(), server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="license_renewal")
    reminders = relationship("Reminder", back_populates="license_renewal")
