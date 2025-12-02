from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.db.session import get_db
from app.core.security import get_current_user
from app.modules.inventory.service import inventory_service
from app.modules.inventory.schemas import (
    IncomingOutgoingRead, IncomingOutgoingCreate, IncomingOutgoingUpdate,
    TransactionMillOperations, TransactionMillOperationsCreate, TransactionMillOperationsUpdate,
    BagDetailsOut, BagReturnRequest
)
from app.modules.users.schemas import UserResponse

router = APIRouter()

# --- Incoming Outgoing ---
@router.get("/incoming_outgoing", response_model=List[IncomingOutgoingRead])
def get_incoming_outgoing(
    brought_by: Optional[str] = None,
    vehicle_no: Optional[str] = None,
    party_through: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    is_incoming: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return inventory_service.get_incoming_outgoing(
        db,
        brought_by=brought_by,
        vehicle_no=vehicle_no,
        party_through=party_through,
        from_date=from_date,
        to_date=to_date,
        is_incoming=is_incoming
    )

@router.get("/incoming_outgoing/{id}", response_model=IncomingOutgoingRead)
def get_incoming_outgoing_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    item = inventory_service.get_incoming_outgoing_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/incoming_outgoing", response_model=IncomingOutgoingRead)
def create_incoming_outgoing(
    item: IncomingOutgoingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return inventory_service.create_incoming_outgoing(db, obj_in=item)

@router.put("/incoming_outgoing/{id}", response_model=IncomingOutgoingRead)
def update_incoming_outgoing(
    id: int,
    item: IncomingOutgoingUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return inventory_service.update_incoming_outgoing(db, id, obj_in=item)

# --- Transactions ---
@router.get("/transactions", response_model=List[TransactionMillOperations])
def get_transactions(
    party_name: Optional[str] = None,
    broker_name: Optional[str] = None,
    transporter_name: Optional[str] = None,
    stock_item_name: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return inventory_service.get_transactions(
        db,
        party_name=party_name,
        broker_name=broker_name,
        transporter_name=transporter_name,
        stock_item_name=stock_item_name,
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type
    )

@router.get("/transactions/{id}", response_model=TransactionMillOperations)
def get_transaction_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    item = inventory_service.get_transaction_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return item

@router.post("/transactions", response_model=TransactionMillOperations)
def create_transaction(
    transaction: TransactionMillOperationsCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return inventory_service.create_transaction(db, transaction)

# @router.put("/transactions/{id}", response_model=TransactionMillOperations)
# def update_transaction(
#     id: int,
#     transaction: TransactionMillOperationsUpdate,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
# ):
#     return inventory_service.update_transaction(db, id, transaction)

@router.get("/stock_summary")
def get_stock_summary(
    godown_name: Optional[str] = None,
    stock_item_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return inventory_service.get_stock_summary(db, godown_name=godown_name, stock_item_name=stock_item_name)

@router.post("/transactions/{id}/return_bags", response_model=List[BagDetailsOut])
def return_bags(
    id: int,
    return_data: List[BagReturnRequest],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return inventory_service.return_bags(db, transaction_id=id, return_data=return_data)
