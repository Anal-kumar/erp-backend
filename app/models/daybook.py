from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime

class DayBook(Base):
    __tablename__ = "daybook"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    ie_date = Column(Date, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    opening_bal = Column(Integer, index=True)
    closing_bal = Column(Integer, index=True)
    party_name = Column(String(30), index=True)
    particular = Column(String(50), index=True)
    is_bank = Column(Boolean, index=True)
    is_receipt = Column(Boolean, index=True)
    amount = Column(Integer, index=True)
    ref_no = Column(String(22), index=True)
    remarks = Column(String(50), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow(), server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="daybook")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None
