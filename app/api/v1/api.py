from fastapi import APIRouter
from app.api.v1.endpoints import events, reminders, daybook, modules, backups, firm_details, labour, setup
from app.modules.auth import router as auth
from app.modules.users import router as users
from app.modules.master_data import router as master_data
from app.modules.inventory import router as inventory
from app.modules.production import router as production

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"]) # Migrated to inventory
api_router.include_router(master_data.router, prefix="/master_data", tags=["master_data"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(production.router, prefix="/production", tags=["production"])
api_router.include_router(events.router, prefix="/events", tags=["events"]) # Events & Announcements
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api_router.include_router(daybook.router, prefix="/daybook", tags=["daybook"])
# api_router.include_router(incoming_outgoing.router, prefix="/incoming_outgoing", tags=["incoming_outgoing"]) # Migrated to inventory
api_router.include_router(modules.router, prefix="/modules", tags=["modules"])
api_router.include_router(backups.router, prefix="/backups", tags=["backups"])
api_router.include_router(firm_details.router, prefix="/firm_details", tags=["firm_details"])
api_router.include_router(labour.router, prefix="/labour", tags=["labour"])
api_router.include_router(setup.router, prefix="", tags=["setup"]) # Setup endpoints (init_db, db/status)
