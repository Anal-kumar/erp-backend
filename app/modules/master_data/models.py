from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base import Base

class PartyDetails(Base):
    __tablename__ = "party_details_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    party_name = Column(String(30), index=True)
    party_mob_no = Column(String(10), index=True)
    party_address = Column(String(30), index=True)
    party_type = Column(String(20), index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    users = relationship("User", back_populates="party_details")
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="party", foreign_keys="[TransactionMillOperations.party_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class BrokerDetails(Base):
    __tablename__ = "broker_details_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    broker_name = Column(String(30), index=True)
    broker_mob_no = Column(String(10), index=True)
    brokerage_rate = Column(Float, index=True, default=0.00)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    users = relationship("User", back_populates="broker_details")
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="broker", foreign_keys="[TransactionMillOperations.broker_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class TransportorDetails(Base):
    __tablename__ = "transportor_details_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    transportor_name = Column(String(30), index=True)
    transportor_mob_no = Column(String(10), index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    users = relationship("User", back_populates="transportor_details")
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="transportor", foreign_keys="[TransactionMillOperations.transportor_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class GodownDetails(Base):
    __tablename__ = "godown_details_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    godown_name = Column(String(30), index=True)
    godown_qtl_capacity = Column(Integer, index=True)
    godown_bags_capacity = Column(Integer, index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    users = relationship("User", back_populates="godown_details")
    transaction_unloading_point_details = relationship("TransactionUnloadingPointDetails", back_populates="godown", foreign_keys="[TransactionUnloadingPointDetails.godown_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class StockItems(Base):
    __tablename__ = "stock_items_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    stock_item_name = Column(String(30), index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    users = relationship("User", back_populates="stock_items")
    transaction_stock_items = relationship("TransactionStockItem", back_populates="stock_items", foreign_keys="[TransactionStockItem.stock_item_id]")
    batch = relationship("Batch", back_populates="stock_items")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class PackagingDetails(Base):
    __tablename__ = "packaging_details_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    packaging_name = Column(String(30), index=True)
    bag_weight = Column(Integer, index=True)
    packaging_unit = Column(String(4), index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    users = relationship("User", back_populates="packaging_details")
    transaction_packaging_details = relationship("TransactionPackagingDetails", back_populates="packaging", foreign_keys="[TransactionPackagingDetails.packaging_id]")
    bag_details = relationship("BagDetails", back_populates="packaging", foreign_keys="[BagDetails.packaging_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

class WeightBridgeOperator(Base):
    __tablename__ = "weight_bridge_operator_operations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    operator_name = Column(String(30), index=True)
    operator_mob_no = Column(String(10), index=True)
    is_active = Column(Boolean, index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)

    users = relationship("User", back_populates="weight_bridge_operator")
    transaction_mill_operations = relationship("TransactionMillOperations", back_populates="weight_bridge_operator", foreign_keys="[TransactionMillOperations.weight_bridge_operator_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None
