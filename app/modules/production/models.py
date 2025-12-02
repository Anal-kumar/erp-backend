from sqlalchemy import Column, Integer, Float, String, Boolean, Time, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class BatchOperator(Base):
    __tablename__ = "batch_operator"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    operator_name = Column(String(30), index=True)
    operator_mob_no = Column(String(10), index=True)
    is_active = Column(Boolean, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="batch_operator")

    first_steam_on = relationship("SteamOn", foreign_keys="SteamOn.first_batch_operator_id", back_populates="first_batch_operator")
    second_steam_on = relationship("SteamOn", foreign_keys="SteamOn.second_batch_operator_id", back_populates="second_batch_operator")

    first_steam_off = relationship("SteamOff", foreign_keys="SteamOff.first_batch_operator_id", back_populates="first_batch_operator")
    second_steam_off = relationship("SteamOff", foreign_keys="SteamOff.second_batch_operator_id", back_populates="second_batch_operator")

    first_drainage = relationship("Drainage", foreign_keys="Drainage.first_batch_operator_id", back_populates="first_batch_operator")
    second_drainage = relationship("Drainage", foreign_keys="Drainage.second_batch_operator_id", back_populates="second_batch_operator")

    first_immersions = relationship("Immerse", foreign_keys="Immerse.first_batch_operator_id", back_populates="first_batch_operator")
    second_immersions = relationship("Immerse", foreign_keys="Immerse.second_batch_operator_id", back_populates="second_batch_operator")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class Clerks(Base):
    __tablename__ = "clerks"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    clerk_name = Column(String(30), index=True)
    clerk_mob_no = Column(String(10), index=True)
    is_active = Column(Boolean, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="clerks")

    cross_verifications_checked = relationship("CrossVerification", foreign_keys="CrossVerification.checker_clerk_id", back_populates="checker_clerk")
    cross_verifications_verified = relationship("CrossVerification", foreign_keys="CrossVerification.verifier_clerk_id", back_populates="verifier_clerk")
    cross_verifications_approved = relationship("CrossVerification", foreign_keys="CrossVerification.approver_clerk_id", back_populates="approver_clerk")

    milling_analysis = relationship("MillingAnalysis", foreign_keys="MillingAnalysis.analyzer_clerk_id", back_populates="analyzer_clerk")

    sorting_analysis_checked = relationship("SortingAnalysis", foreign_keys="SortingAnalysis.checker_clerk_id", back_populates="checker_clerk")
    sorting_analysis_verified = relationship("SortingAnalysis", foreign_keys="SortingAnalysis.verifier_clerk_id", back_populates="verifier_clerk")
    sorting_analysis_analyzed = relationship("SortingAnalysis", foreign_keys="SortingAnalysis.analyzer_clerk_id", back_populates="analyzer_clerk")

    lot_details_checker = relationship("LotDetails", back_populates="checker_clerk", foreign_keys="[LotDetails.checker_clerk_id]")
    lot_details_verifier = relationship("LotDetails", back_populates="verifier_clerk", foreign_keys="[LotDetails.verifier_clerk_id]")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_name = Column(String(30), index=True)
    batch_date = Column(Date, index=True)
    pot_number = Column(Integer, index=True)
    stock_item_id = Column(Integer, ForeignKey("stock_items_operations.id"), index=True)
    stock_quantity = Column(Integer, default=0) # Bags
    stock_weight = Column(Float, default=0.0) # KG (as per legacy schema, though user said quintal for calc, legacy stores KG?)
    # Checking legacy batch_operations.py: stock_weight=batch.stock_weight (KG). 
    # But calculation uses / 100.0 for quintal. So DB stores KG.
    
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    cross_verification = relationship("CrossVerification", back_populates="batch")
    drainage = relationship("Drainage", back_populates="batch")
    immerse = relationship("Immerse", back_populates="batch")
    milling_analysis = relationship("MillingAnalysis", back_populates="batch")
    steam_on = relationship("SteamOn", back_populates="batch")
    steam_off = relationship("SteamOff", back_populates="batch")
    sorting_analysis = relationship("SortingAnalysis", back_populates="batch")
    stock_items = relationship(
        "app.modules.master_data.models.StockItems",
        back_populates="batch",
    )
    users = relationship("app.modules.users.models.User", back_populates="batch")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None

    @hybrid_property
    def stock_item_name(self):
        return self.stock_items.stock_item_name if self.stock_items else None


class SteamOn(Base):
    __tablename__ = "steam_on"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    steam_on_date = Column(Date, index=True)
    steam_on_time = Column(Time, index=True)
    first_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    second_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="steam_on")
    batch = relationship("Batch", back_populates="steam_on")
    first_batch_operator = relationship("BatchOperator", foreign_keys=[first_batch_operator_id], back_populates="first_steam_on")
    second_batch_operator = relationship("BatchOperator", foreign_keys=[second_batch_operator_id], back_populates="second_steam_on")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class SteamOff(Base):
    __tablename__ = "steam_off"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    steam_off_date = Column(Date, index=True)
    steam_off_time = Column(Time, index=True)
    first_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    second_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="steam_off")
    batch = relationship("Batch", back_populates="steam_off")
    first_batch_operator = relationship("BatchOperator", foreign_keys=[first_batch_operator_id], back_populates="first_steam_off")
    second_batch_operator = relationship("BatchOperator", foreign_keys=[second_batch_operator_id], back_populates="second_steam_off")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class Drainage(Base):
    __tablename__ = "drainage"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    drainage_date = Column(Date, index=True)
    drainage_time = Column(Time, index=True)
    first_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    second_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="drainage")
    batch = relationship("Batch", back_populates="drainage")
    first_batch_operator = relationship("BatchOperator", foreign_keys=[first_batch_operator_id], back_populates="first_drainage")
    second_batch_operator = relationship("BatchOperator", foreign_keys=[second_batch_operator_id], back_populates="second_drainage")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class Immerse(Base):
    __tablename__ = "immerse"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    immersion_date = Column(Date, index=True)
    immersion_time = Column(Time, index=True)
    first_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    second_batch_operator_id = Column(Integer, ForeignKey("batch_operator.id"), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="immerse")
    batch = relationship("Batch", back_populates="immerse")
    first_batch_operator = relationship("BatchOperator", foreign_keys=[first_batch_operator_id], back_populates="first_immersions")
    second_batch_operator = relationship("BatchOperator", foreign_keys=[second_batch_operator_id], back_populates="second_immersions")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class MillingAnalysis(Base):
    __tablename__ = "milling_analysis"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    analyzer_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    milling_rice_moisture_percent = Column(Float, index=True)
    milling_broken_percent = Column(Float, index=True)
    milling_discolor_percent = Column(Float, index=True)
    milling_damaged_percent = Column(Float, index=True)
    milling_output_porridge_30sec = Column(Float, index=True)
    milling_output_final_polisher_30sec = Column(Float, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="milling_analysis")
    batch = relationship("Batch", back_populates="milling_analysis")
    analyzer_clerk = relationship("Clerks", foreign_keys=[analyzer_clerk_id], back_populates="milling_analysis")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class SortingAnalysis(Base):
    __tablename__ = "sorting_analysis"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    analyzer_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    sorted_rice_moisture_percent = Column(Float, index=True)
    sorted_broken_percent = Column(Float, index=True)
    sorted_discolor_percent = Column(Float, index=True)
    sorted_damaged_percent = Column(Float, index=True)
    rejection_rice_percent = Column(Float, index=True)
    sorting_output_30sec = Column(Float, index=True)
    rejection_output_30sec = Column(Float, index=True)
    checker_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    checking_date = Column(Date, index=True)
    checking_time = Column(Time, index=True)
    verifier_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    verifying_date = Column(Date, index=True)
    verifying_time = Column(Time, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="sorting_analysis")
    batch = relationship("Batch", back_populates="sorting_analysis")
    analyzer_clerk = relationship("Clerks", foreign_keys=[analyzer_clerk_id], back_populates="sorting_analysis_analyzed")
    checker_clerk = relationship("Clerks", foreign_keys=[checker_clerk_id], back_populates="sorting_analysis_checked")
    verifier_clerk = relationship("Clerks", foreign_keys=[verifier_clerk_id], back_populates="sorting_analysis_verified")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class CrossVerification(Base):
    __tablename__ = "cross_verification"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    checker_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    checking_date = Column(Date, index=True)
    checking_time = Column(Time, index=True)
    verifier_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    verifying_date = Column(Date, index=True)
    verifying_time = Column(Time, index=True)
    paddy_moisture_percent = Column(Float, index=True)
    approver_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="cross_verification")
    batch = relationship("Batch", back_populates="cross_verification")
    checker_clerk = relationship("Clerks", foreign_keys=[checker_clerk_id], back_populates="cross_verifications_checked")
    verifier_clerk = relationship("Clerks", foreign_keys=[verifier_clerk_id], back_populates="cross_verifications_verified")
    approver_clerk = relationship("Clerks", foreign_keys=[approver_clerk_id], back_populates="cross_verifications_approved")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


class LotDetails(Base):
    __tablename__ = "lot_details"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    lot_number = Column(Integer, index=True)
    lot_moisture_percent = Column(Float, index=True)
    lot_broken_percent = Column(Float, index=True)
    lot_discolor_percent = Column(Float, index=True)
    lot_damaged_percent = Column(Float, index=True)
    lot_lower_grain_percent = Column(Float, index=True)
    lot_chalky_percent = Column(Float, index=True)
    lot_frk_percent = Column(Float, index=True)
    lot_other_percent = Column(Float, index=True)
    checker_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    checking_date = Column(Date, index=True)
    checking_time = Column(Time, index=True)
    verifier_clerk_id = Column(Integer, ForeignKey("clerks.id"), index=True)
    verifying_date = Column(Date, index=True)
    verifying_time = Column(Time, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(DateTime(timezone=True), default=datetime.utcnow, server_default=func.now(), onupdate=func.now())

    users = relationship("app.modules.users.models.User", back_populates="lot_details")
    checker_clerk = relationship("Clerks", foreign_keys=[checker_clerk_id], back_populates="lot_details_checker")
    verifier_clerk = relationship("Clerks", foreign_keys=[verifier_clerk_id], back_populates="lot_details_verifier")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None
    
    @hybrid_property
    def checker_clerk_name(self):
        return self.checker_clerk.clerk_name if self.checker_clerk else None
    
    @hybrid_property
    def verifier_clerk_name(self):
        return self.verifier_clerk.clerk_name if self.verifier_clerk else None
