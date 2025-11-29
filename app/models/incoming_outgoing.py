from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime

class IncomingOutgoing(Base):
    __tablename__ = "incoming_outgoing"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    io_date = Column(Date, index=True)
    is_incoming = Column(Boolean, index=True)
    rst_bill = Column(String(20), index=True)
    brought_by = Column(String(30), index=True)
    mob_no = Column(String(10), index=True)
    vehicle_no = Column(String(11), index=True)
    origin = Column(String(30), index=True)
    party_through = Column(String(30), index=True)
    transportation_expense = Column(Integer, index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow(), server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="incoming_outgoing")
    incoming_outgoing_items = relationship("IncomingOutgoingItems", back_populates="incoming_outgoing", foreign_keys="[IncomingOutgoingItems.incoming_outgoing_id]")
    incoming_outgoing_payment = relationship("IncomingOutgoingPayment", back_populates="incoming_outgoing", foreign_keys="[IncomingOutgoingPayment.incoming_outgoing_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class IncomingOutgoingItems(Base):
    __tablename__ = "incoming_outgoing_items"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    incoming_outgoing_id = Column(Integer, ForeignKey("incoming_outgoing.id", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    jins = Column(String(30), index=True)
    bags_no = Column(Boolean, index=True)
    quantity = Column(Integer, index=True)
    packaging = Column(String(30), index=True)
    weight_society = Column(Integer, index=True)
    weight_wb = Column(Integer, index=True)
    amount = Column(Integer, index=True)

    incoming_outgoing = relationship("IncomingOutgoing", back_populates="incoming_outgoing_items")

class IncomingOutgoingPayment(Base):
    __tablename__ = "incoming_outgoing_payment"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    incoming_outgoing_id = Column(Integer, ForeignKey("incoming_outgoing.id", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    payment_amount = Column(Integer, index=True)
    payment_date = Column(Date, index=True, nullable=True)

    incoming_outgoing = relationship("IncomingOutgoing", back_populates="incoming_outgoing_payment")
