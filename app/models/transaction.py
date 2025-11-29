from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime
import enum

class TransactionMillOperations(Base):
    __tablename__ = "transaction_mill_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    rst_number = Column(String(20), index=True)
    bill_number = Column(String(20), index=True)
    transaction_date = Column(Date, index=True)
    transaction_type = Column(Boolean, index=True)  # True for Purchase, False for Sales
    party_id = Column(Integer, ForeignKey("party_details_operations.id"), index=True)
    broker_id = Column(Integer, ForeignKey("broker_details_operations.id"), index=True)
    transportor_id = Column(Integer, ForeignKey("transportor_details_operations.id"), index=True)
    gross_weight = Column(Integer, index=True)
    tare_weight = Column(Integer, index=True)
    weight_bridge_operator_id = Column(Integer, ForeignKey("weight_bridge_operator_operations.id"), index=True)
    vehicle_number = Column(String(10), index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow(), server_default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="transaction_mill_operations")

    party = relationship("PartyDetails", back_populates="transaction_mill_operations", foreign_keys=[party_id], lazy='joined')
    broker = relationship("BrokerDetails", back_populates="transaction_mill_operations", foreign_keys=[broker_id], lazy='joined')
    transportor = relationship("TransportorDetails", back_populates="transaction_mill_operations", foreign_keys=[transportor_id], lazy='joined')
    weight_bridge_operator = relationship("WeightBridgeOperator", back_populates="transaction_mill_operations", foreign_keys=[weight_bridge_operator_id], lazy='joined')
    
    transaction_packaging_details = relationship(
        "TransactionPackagingDetails",
        back_populates="transaction_mill_operations",
        foreign_keys="TransactionPackagingDetails.transaction_id",
        cascade="all, delete-orphan"
    )

    transaction_stock_items = relationship(
        "TransactionStockItem",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan",
        foreign_keys="TransactionStockItem.transaction_id"
    )

    transaction_allowance_deduction_details = relationship(
        "TransactionAllowanceDeductionsDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan",
        foreign_keys="TransactionAllowanceDeductionsDetails.transaction_id"
    )
    
    transaction_payments_mill_operations = relationship(
        "TransactionPaymentDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan",
        foreign_keys="TransactionPaymentDetails.transaction_id"
    )
    transaction_unloading_point_details = relationship(
        "TransactionUnloadingPointDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan",
        foreign_keys="TransactionUnloadingPointDetails.transaction_id"
    )

    bag_details = relationship(
        "BagDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan",
        foreign_keys="BagDetails.transaction_id"
    )

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class TransactionPackagingDetails(Base):
    __tablename__ = "transaction_packaging_details_mill_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    packaging_id = Column(Integer, ForeignKey("packaging_details_operations.id"), index=True)
    bag_nos = Column(Integer, index=True)

    packaging = relationship("PackagingDetails", back_populates="transaction_packaging_details", foreign_keys=[packaging_id])
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_packaging_details", foreign_keys=[transaction_id])

class TransactionStockItem(Base):
    __tablename__ = "transaction_stock_items_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    stock_item_id = Column(Integer, ForeignKey("stock_items_operations.id"), index=True)
    number_of_bags = Column(Integer, index=True)
    weight = Column(Float, index=True)
    rate = Column(Float, index=True)

    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_stock_items", foreign_keys=[transaction_id])
    stock_items = relationship("StockItems", back_populates="transaction_stock_items", foreign_keys=[stock_item_id])

class TransactionAllowanceDeductionsDetails(Base):
    __tablename__ = "transaction_allowances_deduction_mill_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    is_allowance = Column(Boolean, index=True)
    allowance_deduction_name = Column(String(20), index=True)
    allowance_deduction_amount = Column(Integer, index=True)
    remarks = Column(String(50), index=True)

    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_allowance_deduction_details", foreign_keys=[transaction_id])

class TransactionPaymentDetails(Base):
    __tablename__ = "transaction_payments_mill_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    payment_amount = Column(Float, index=True)
    payment_date = Column(Date, index=True)
    payment_remarks = Column(String(50), index=True)

    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_payments_mill_operations", foreign_keys=[transaction_id])

class TransactionUnloadingPointDetails(Base):
    __tablename__ = "transaction_unloading_point_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    godown_id = Column(Integer, ForeignKey("godown_details_operations.id"), index=True)
    number_of_bags = Column(Integer, index=True) 
    remarks = Column(String(50), index=True)

    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_unloading_point_details", foreign_keys=[transaction_id])
    godown = relationship("GodownDetails", back_populates="transaction_unloading_point_details", foreign_keys=[godown_id])

class BagsStatus(enum.Enum):
    ACTIVE = "active"
    RETURNED = "returned"

class BagDetails(Base):
    __tablename__ = "bag_details"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    packaging_id = Column(Integer, ForeignKey("packaging_details_operations.id", ondelete="CASCADE"), index=True)
    total_bags = Column(Integer, index=True)
    returned_bags = Column(Integer, index=True)
    remaining_bags = Column(Integer, index=True)
    bags_status = Column(Enum(BagsStatus), default=BagsStatus.ACTIVE, index=True)

    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="bag_details")
    packaging = relationship("PackagingDetails", back_populates="bag_details")

    @hybrid_property
    def packaging_name(self):
        return self.packaging.packaging_name if self.packaging else None
