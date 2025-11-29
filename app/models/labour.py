from sqlalchemy import Column, Boolean, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


# ============================================================
# Voucher Header Table (remains same)
# ============================================================
class LabourPaymentVouchers(Base):
    __tablename__ = "vouchers_labour_payments"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    vch_date = Column(Date, index=True)
    remarks = Column(String(50), index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    time_stamp = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relationship to user (must exist in User model)
    users = relationship("User", back_populates="labour_payment_vouchers")

    # association (detail) relationships
    voucher_gangs = relationship("VoucherGang", back_populates="voucher", foreign_keys="VoucherGang.voucher_labour_payment_id", cascade="all, delete-orphan")

    voucher_work_items = relationship("VoucherWorkItem", back_populates="voucher", foreign_keys="VoucherWorkItem.voucher_labour_payment_id", cascade="all, delete-orphan")

    voucher_particulars = relationship("VoucherParticular", back_populates="voucher", foreign_keys="VoucherParticular.voucher_labour_payment_id", cascade="all, delete-orphan")

    voucher_bag_packagings = relationship("VoucherBagPackaging", back_populates="voucher", foreign_keys="VoucherBagPackaging.voucher_labour_payment_id", cascade="all, delete-orphan")

    voucher_locations = relationship("VoucherLocation", back_populates="voucher", foreign_keys="VoucherLocation.voucher_labour_payment_id", cascade="all, delete-orphan")

    @hybrid_property
    def user_login(self):
        return self.users.user_login_id if self.users else None


# ============================================================
# Master Tables (remain same)
# ============================================================

class LabourGang(Base):
    __tablename__ = "labour_gang"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    gang_name = Column(String(30), index=True)
    gang_mob_no = Column(String(10), index=True)
    work_rate = Column(Float, index=True)
    is_active = Column(Boolean, index=True)
    remarks = Column(String(50), index=True)

    voucher_gangs = relationship("VoucherGang", back_populates="gang")


class LabourWorkItem(Base):
    __tablename__ = "labour_work_item"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    labour_item_name = Column(String(30), index=True)
    remarks = Column(String(50), index=True)

    # labour_payment_vouchers = relationship("LabourPaymentVouchers", back_populates="labour_work_item")


class LabourWorkParticulars(Base):
    __tablename__ = "labour_work_particulars"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    work_name = Column(String(30), index=True)
    remarks = Column(String(50), index=True)

    # labour_payment_vouchers = relationship("LabourPaymentVouchers", back_populates="labour_work_particulars")


class LabourBagPackagingWeight(Base):
    __tablename__ = "labour_bag_packaging_weight"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    bag_weight = Column(Integer, index=True)
    remarks = Column(String(50), index=True)

    # labour_payment_vouchers = relationship("LabourPaymentVouchers", back_populates="labour_bag_packaging_weight")


class LabourWorkLocation(Base):
    __tablename__ = "labour_work_location"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    work_locations = Column(String(30), index=True)
    remarks = Column(String(50), index=True)


# ============================================================
# Association Tables (new)
# ============================================================

class VoucherGang(Base):
    __tablename__ = "voucher_gangs"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    voucher_labour_payment_id = Column(Integer, ForeignKey("vouchers_labour_payments.id", ondelete="CASCADE"), index=True)
    gang_id = Column(Integer, ForeignKey("labour_gang.id"), index=True)
    work_rate = Column(Float, index=True)

    voucher = relationship("LabourPaymentVouchers", back_populates="voucher_gangs")
    gang = relationship("LabourGang", back_populates="voucher_gangs")

class VoucherWorkItem(Base):
    __tablename__ = "voucher_work_items"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    voucher_labour_payment_id = Column(Integer, ForeignKey("vouchers_labour_payments.id", ondelete="CASCADE"), index=True)
    work_item_id = Column(Integer, ForeignKey("labour_work_item.id"), index=True)

    voucher = relationship("LabourPaymentVouchers", back_populates="voucher_work_items")
    work_item = relationship("LabourWorkItem")


class VoucherParticular(Base):
    __tablename__ = "voucher_particulars"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    voucher_labour_payment_id = Column(Integer, ForeignKey("vouchers_labour_payments.id", ondelete="CASCADE"), index=True)
    particulars_id = Column(Integer, ForeignKey("labour_work_particulars.id"), index=True)

    voucher = relationship("LabourPaymentVouchers", back_populates="voucher_particulars")
    particular = relationship("LabourWorkParticulars")


class VoucherBagPackaging(Base):
    __tablename__ = "voucher_bag_packagings"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    voucher_labour_payment_id = Column(Integer, ForeignKey("vouchers_labour_payments.id", ondelete="CASCADE"), index=True)
    bag_packaging_id = Column(Integer, ForeignKey("labour_bag_packaging_weight.id"), index=True)
    bags_nos = Column(Integer, index=True)
    gang_id = Column(Integer, ForeignKey("labour_gang.id"), nullable=True, index=True)

    voucher = relationship("LabourPaymentVouchers", back_populates="voucher_bag_packagings")
    bag_packaging = relationship("LabourBagPackagingWeight")
    gang = relationship("LabourGang")


class VoucherLocation(Base):
    __tablename__ = "voucher_locations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    voucher_labour_payment_id = Column(Integer, ForeignKey("vouchers_labour_payments.id", ondelete="CASCADE"), index=True)
    labour_work_location_id_origin = Column(Integer, ForeignKey("labour_work_location.id"), index=True)
    labour_work_location_id_destination = Column(Integer, ForeignKey("labour_work_location.id"), index=True)
    

    voucher = relationship("LabourPaymentVouchers", back_populates="voucher_locations")
    location_origin = relationship(
        "LabourWorkLocation",
        foreign_keys=[labour_work_location_id_origin]
    )
    location_destination = relationship(
        "LabourWorkLocation",
        foreign_keys=[labour_work_location_id_destination]
    )
