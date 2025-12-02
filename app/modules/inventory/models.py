import enum
from typing import Optional
from sqlalchemy import Column, Integer, Float, String, Boolean, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime

class BagsStatus(enum.Enum):
    ACTIVE = "active"
    RETURNED = "returned"

# Model for Incoming and Outgoing
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
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    # Relationship to User and IncomingOutgoingItems
    users = relationship("app.modules.users.models.User", back_populates="incoming_outgoing")
    incoming_outgoing_items = relationship("IncomingOutgoingItems", back_populates="incoming_outgoing", cascade="all, delete-orphan")
    incoming_outgoing_payment = relationship("IncomingOutgoingPayment", back_populates="incoming_outgoing", cascade="all, delete-orphan")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

# Model for Incoming and Outgoing Items
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

    # Relationship to IncomingOutgoing
    incoming_outgoing = relationship("IncomingOutgoing", back_populates="incoming_outgoing_items")

# Model for Incoming and Outgoing Payment
class IncomingOutgoingPayment(Base):
    __tablename__ = "incoming_outgoing_payment"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    incoming_outgoing_id = Column(Integer, ForeignKey("incoming_outgoing.id", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    payment_amount = Column(Integer, index=True)
    payment_date = Column(Date, index=True, nullable=True)

    # Relationship to IncomingOutgoing
    incoming_outgoing = relationship("IncomingOutgoing", back_populates="incoming_outgoing_payment")

class StockLedger(Base):
    __tablename__ = "stock_ledger"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    godown_id = Column(Integer, ForeignKey("godown_details_operations.id"), index=True)
    stock_item_id = Column(Integer, ForeignKey("stock_items_operations.id"), index=True)
    stock_quantity_bags = Column(Integer, default=0)  # Bags
    stock_weight_quintal = Column(Float, default=0.0)  # Quintals
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    godown = relationship("app.modules.master_data.models.GodownDetails")
    stock_item = relationship("app.modules.master_data.models.StockItems")

    def apply_stock_movement(self, transaction_type: Optional[bool], bags: int, weight_quintal: float):
        """
        Updates the stock ledger based on transaction type.
        :param transaction_type: True = Purchase (add), False = Sale (subtract)
        :param bags: number of bags moved
        :param weight_quintal: weight in quintals moved
        """
        if transaction_type:  # Purchase / Incoming
            self.stock_quantity_bags = (self.stock_quantity_bags or 0) + bags
            self.stock_weight_quintal = (self.stock_weight_quintal or 0.0) + weight_quintal
        else:  # Sale / Outgoing
            self.stock_quantity_bags = (self.stock_quantity_bags or 0) - bags
            self.stock_weight_quintal = (self.stock_weight_quintal or 0.0) - weight_quintal


    @hybrid_property
    def godown_name(self):
        return self.godown.godown_name if self.godown else None

# Model for Transaction Mill Operations
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

    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship("app.modules.users.models.User", back_populates="transaction_mill_operations")

    party = relationship("app.modules.master_data.models.PartyDetails", back_populates="transaction_mill_operations", lazy='joined')
    broker = relationship("app.modules.master_data.models.BrokerDetails", back_populates="transaction_mill_operations", lazy='joined')
    transportor = relationship("app.modules.master_data.models.TransportorDetails", back_populates="transaction_mill_operations", lazy='joined')
    weight_bridge_operator = relationship("app.modules.master_data.models.WeightBridgeOperator", back_populates="transaction_mill_operations", lazy='joined')
    
    transaction_packaging_details = relationship(
        "TransactionPackagingDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan"
    )

    transaction_stock_items = relationship(
        "TransactionStockItem",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan"
    )

    transaction_allowance_deduction_details = relationship(
        "TransactionAllowanceDeductionsDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan"
    )
    
    transaction_payments_mill_operations = relationship(
        "TransactionPaymentDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan"
    )
    transaction_unloading_point_details = relationship(
        "TransactionUnloadingPointDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan"
    )

    bag_details = relationship(
        "BagDetails",
        back_populates="transaction_mill_operations",
        cascade="all, delete-orphan"
    )

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

# Model for Transaction Packaging Details
class TransactionPackagingDetails(Base):
    __tablename__ = "transaction_packaging_details_mill_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    packaging_id = Column(Integer, ForeignKey("packaging_details_operations.id"), index=True)
    bag_nos = Column(Integer, index=True)

    # Relationship to TransactionMillOperations
    packaging = relationship("app.modules.master_data.models.PackagingDetails", back_populates="transaction_packaging_details")
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_packaging_details")

# Model for Transaction Stock Item
class TransactionStockItem(Base):
    __tablename__ = "transaction_stock_items_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    stock_item_id = Column(Integer, ForeignKey("stock_items_operations.id"), index=True)
    number_of_bags = Column(Integer, index=True)
    weight = Column(Float, index=True)
    rate = Column(Float, index=True)

    # Relationship to TransactionMillOperations
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_stock_items")
    stock_items = relationship("app.modules.master_data.models.StockItems", back_populates="transaction_stock_items")


# Model for Transaction Allowance Details
class TransactionAllowanceDeductionsDetails(Base):
    __tablename__ = "transaction_allowances_deduction_mill_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    is_allowance = Column(Boolean, index=True)
    allowance_deduction_name = Column(String(20), index=True)
    allowance_deduction_amount = Column(Integer, index=True)
    remarks = Column(String(50), index=True)

    # Relationship to TransactionMillOperations
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_allowance_deduction_details")

# Model for Transaction Payment Details
class TransactionPaymentDetails(Base):
    __tablename__ = "transaction_payments_mill_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    payment_amount = Column(Float, index=True)
    payment_date = Column(Date, index=True)
    payment_remarks = Column(String(50), index=True)

    # Relationship to TransactionMillOperations
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_payments_mill_operations")

# Model for Transaction unloading point details
class TransactionUnloadingPointDetails(Base):
    __tablename__ = "transaction_unloading_point_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_mill_operations.id", ondelete="CASCADE"), index=True)
    godown_id = Column(Integer, ForeignKey("godown_details_operations.id"), index=True)
    number_of_bags = Column(Integer, index=True) 
    remarks = Column(String(50), index=True)

    # Relationship to TransactionMillOperations
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transaction_unloading_point_details")
    godown = relationship("app.modules.master_data.models.GodownDetails", back_populates="transaction_unloading_point_details")

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
    packaging = relationship("app.modules.master_data.models.PackagingDetails", back_populates="bag_details")


    @hybrid_property
    def packaging_name(self):
        return self.packaging.packaging_name if self.packaging else None
