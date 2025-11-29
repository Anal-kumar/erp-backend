from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_login_id = Column(String(30), unique=True, index=True)
    user_first_name = Column(String(30), index=True)
    user_second_name = Column(String(30), index=True)
    mobile_number = Column(String(10), index=True)
    designation = Column(String(30), index=True)
    user_role = Column(String(15), default=False)
    password = Column(String(100), index=True)
    time_stamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now(), onupdate=func.now())

    # Relationships
    reminders = relationship("Reminder", back_populates="users")
    daybook = relationship("DayBook", back_populates="users")
    incoming_outgoing = relationship("IncomingOutgoing", back_populates="users")
    party_details = relationship("PartyDetails", back_populates="users")
    broker_details = relationship("BrokerDetails", back_populates="users")
    transportor_details = relationship("TransportorDetails", back_populates="users")
    godown_details = relationship("GodownDetails", back_populates="users")
    stock_items = relationship("StockItems", back_populates="users")
    packaging_details = relationship("PackagingDetails", back_populates="users")
    weight_bridge_operator = relationship("WeightBridgeOperator", back_populates="users")
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="users")
    # labour_payment_vouchers = relationship("LabourPaymentVouchers", back_populates="users") # TODO: Fix import path later
    module_control = relationship("ModuleControl", back_populates="users")
    license_renewal = relationship("LicenseRenewal", back_populates="users")
    
    batch = relationship("Batch", back_populates="users")
    batch_operator = relationship("BatchOperator", back_populates="users")    
    immerse = relationship("Immerse", back_populates="users")
    clerks = relationship("Clerks", back_populates="users")
    lot_details = relationship("LotDetails", back_populates="users")
    drainage = relationship("Drainage", back_populates="users")
    steam_on = relationship("SteamOn", back_populates="users")
    steam_off = relationship("SteamOff", back_populates="users")
    cross_verification = relationship("CrossVerification", back_populates="users")
    milling_analysis = relationship("MillingAnalysis", back_populates="users")
    sorting_analysis = relationship("SortingAnalysis", back_populates="users")

