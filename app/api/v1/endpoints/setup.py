from fastapi import APIRouter, Response, status, Body, Depends
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from urllib.parse import urlparse
import os
from datetime import date

from app.db.session import engine, SessionLocal, get_db
from app.core.config import settings
from app.core.security import hash_password
from app.db.base import Base
import app.modules.users.schemas as user_schemas
from app.modules.users.models import User
from app.models.module import ModuleControl
from app.models.daybook import DayBook
from app.modules.master_data.models import TransportorDetails, BrokerDetails

router = APIRouter()

@router.get("/db/status")
async def db_status():
    # Extract the raw file path from the SQLAlchemy URL
    raw_path = urlparse(settings.SQLALCHEMY_DATABASE_URL).path.lstrip("/")
    db_path = os.path.normpath(raw_path)

    # Just check if the DB file exists
    if os.path.exists(db_path):
        return { "db_initialized": True, "message": "Database already initialized." }
    return { "db_initialized": False}

@router.post("/init_db")
async def init(admin_user: user_schemas.UserCreate = Body(...)):
    raw_path = urlparse(settings.SQLALCHEMY_DATABASE_URL).path.lstrip("/")
    db_path = os.path.normpath(raw_path)

    inspector = inspect(engine)
    # Ensure metadata is bound
    Base.metadata.bind = engine
    expected_tables = set(Base.metadata.tables.keys())
    existing_tables = set(inspector.get_table_names())

    # ✅ DB already initialized
    if os.path.exists(db_path) and expected_tables.issubset(existing_tables):
        return Response(status_code=status.HTTP_200_OK, content="Database already initialized!")

    # ✅ Create tables
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    Base.metadata.create_all(bind=engine)

    # ✅ Seed initial data
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.user_login_id == 'superadmin').first()

        if not existing_user:
            # Super admin
            super_admin = User(
                user_login_id="superadmin",
                user_first_name="Super",
                user_second_name="Admin",
                mobile_number="1234567890",
                designation="Super Administrator",
                user_role="superadmin",
                password=hash_password("superadmin123")
            )
            db.add(super_admin)
            db.commit()
            db.refresh(super_admin)

            # Admin user (from frontend payload)
            new_admin = User(
                user_login_id=admin_user.user_login_id,
                user_first_name=admin_user.user_first_name,
                user_second_name=admin_user.user_second_name,
                mobile_number=admin_user.mobile_number,
                designation=admin_user.designation,
                user_role=admin_user.user_role,
                password=hash_password(admin_user.password)
            )
            db.add(new_admin)
            db.commit()

            # Default modules (linked to super_admin)
            modules = [
                ModuleControl(user_login_id=super_admin.id, module_name="mill_operations", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="incoming", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="outgoing", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="day_book", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="expiry_reminder", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="users", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="labour_payment", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="batch_operations", module_enabled=False),
                ModuleControl(user_login_id=super_admin.id, module_name="lot_operations", module_enabled=False),
            ]
            db.add_all(modules)
            db.commit()

            # Initial DayBook entry
            db_daybook = DayBook(
                ie_date=date.today(),
                user_login_id=super_admin.id,
                party_name="Self",
                particular="Opening Balance",
                is_bank=False,
                is_receipt=False,
                amount=0,
                ref_no="Opening Balance",
                remarks="Opening Balance",
                closing_bal=0,
                opening_bal=0
            )
            db.add(db_daybook)
            db.commit()

            # Initial Transporter
            db_transporter = TransportorDetails(
                transportor_name="Self",
                transportor_mob_no="0000000000",
                remarks="Self",
                user_login_id=super_admin.id
            )

            db.add(db_transporter)
            db.commit()

            # Initial Broker
            db_broker = BrokerDetails(
                broker_name="Self",
                broker_mob_no="0000000000",
                brokerage_rate=0.00,
                remarks="Self",
                user_login_id=super_admin.id
            )

            db.add(db_broker)
            db.commit()

        return Response(content="Database initialized successfully!", status_code=status.HTTP_201_CREATED)

    finally:
        db.close()
