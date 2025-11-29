from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.security import get_current_user
from app.modules.master_data import schemas
from app.modules.master_data.service import (
    party_service, broker_service, transportor_service,
    godown_service, stock_item_service, packaging_service,
    weight_bridge_operator_service
)

router = APIRouter()

# --- Party Details ---
@router.get("/get_party_details", response_model=List[schemas.PartyDetails], tags=["Party Details"])
def get_party_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    party_name: Optional[str] = None,
):
    if party_name:
        # Custom filter not in generic service yet, accessing repo directly or adding method to service
        # For now, let's just do what we did before but using service/repo
        return db.query(party_service.repository.model).filter(
            party_service.repository.model.party_name.ilike(f"%{party_name}%")
        ).all()
    return party_service.get_multi(db)

@router.get("/get_party_details/{party_id}", response_model=schemas.PartyDetails, tags=["Party Details"])
def get_party_detail(party_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    party = party_service.get(db, id=party_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party Details not found")
    return party

@router.post("/create_party_details", response_model=schemas.PartyDetails, tags=["Party Details"])
def create_party_details(party: schemas.PartyCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return party_service.create(db, obj_in=party)

@router.put("/update_party_details/{party_id}", response_model=schemas.PartyDetails, tags=["Party Details"])
def update_party_details(party_id: int, party: schemas.PartyUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_party = party_service.get(db, id=party_id)
    if not db_party:
        raise HTTPException(status_code=404, detail="Party Details not found")
    return party_service.update(db, db_obj=db_party, obj_in=party)

# --- Broker Details ---
@router.get("/get_broker_details", response_model=List[schemas.BrokerDetails], tags=["Broker Details"])
def get_broker_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    broker_name: Optional[str] = None,
):
    if broker_name:
        return db.query(broker_service.repository.model).filter(
            broker_service.repository.model.broker_name.ilike(f"%{broker_name}%")
        ).all()
    return broker_service.get_multi(db)

@router.get("/get_broker_details/{broker_id}", response_model=schemas.BrokerDetails, tags=["Broker Details"])
def get_broker_detail(broker_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    broker = broker_service.get(db, id=broker_id)
    if not broker:
        raise HTTPException(status_code=404, detail="Broker Details not found")
    return broker

@router.post("/create_broker_details", response_model=schemas.BrokerDetails, tags=["Broker Details"])
def create_broker_details(broker: schemas.BrokerCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return broker_service.create(db, obj_in=broker)

@router.put("/update_broker_details/{broker_id}", response_model=schemas.BrokerDetails, tags=["Broker Details"])
def update_broker_details(broker_id: int, broker: schemas.BrokerUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_broker = broker_service.get(db, id=broker_id)
    if not db_broker:
        raise HTTPException(status_code=404, detail="Broker Details not found")
    return broker_service.update(db, db_obj=db_broker, obj_in=broker)

# --- Transporter Details ---
@router.get("/get_transportor_details", response_model=List[schemas.TransportorDetails], tags=["Transportor Details"])
def get_transportor_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    transportor_name: Optional[str] = None,
):
    if transportor_name:
        return db.query(transportor_service.repository.model).filter(
            transportor_service.repository.model.transportor_name.ilike(f"%{transportor_name}%")
        ).all()
    return transportor_service.get_multi(db)

@router.get("/get_transportor_details/{transportor_id}", response_model=schemas.TransportorDetails, tags=["Transportor Details"])
def get_transportor_detail(transportor_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    transportor = transportor_service.get(db, id=transportor_id)
    if not transportor:
        raise HTTPException(status_code=404, detail="Transportor Details not found")
    return transportor

@router.post("/create_transportor_details", response_model=schemas.TransportorDetails, tags=["Transportor Details"])
def create_transportor_details(transportor: schemas.TransportorCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return transportor_service.create(db, obj_in=transportor)

@router.put("/update_transportor_details/{transportor_id}", response_model=schemas.TransportorDetails, tags=["Transportor Details"])
def update_transportor_details(transportor_id: int, transportor: schemas.TransportorUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_transportor = transportor_service.get(db, id=transportor_id)
    if not db_transportor:
        raise HTTPException(status_code=404, detail="Transportor Details not found")
    return transportor_service.update(db, db_obj=db_transportor, obj_in=transportor)

# --- Godown Details ---
@router.get("/get_godown_details", response_model=List[schemas.GodownDetails], tags=["Godown Details"])
def get_godown_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    godown_name: Optional[str] = None,
):
    if godown_name:
        return db.query(godown_service.repository.model).filter(
            godown_service.repository.model.godown_name.ilike(f"%{godown_name}%")
        ).all()
    return godown_service.get_multi(db)

@router.get("/get_godown_details/{godown_id}", response_model=schemas.GodownDetails, tags=["Godown Details"])
def get_godown_detail(godown_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    godown = godown_service.get(db, id=godown_id)
    if not godown:
        raise HTTPException(status_code=404, detail="Godown Details not found")
    return godown

@router.post("/create_godown_details", response_model=schemas.GodownDetails, tags=["Godown Details"])
def create_godown_details(godown: schemas.GodownCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return godown_service.create(db, obj_in=godown)

@router.put("/update_godown_details/{godown_id}", response_model=schemas.GodownDetails, tags=["Godown Details"])
def update_godown_details(godown_id: int, godown: schemas.GodownUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_godown = godown_service.get(db, id=godown_id)
    if not db_godown:
        raise HTTPException(status_code=404, detail="Godown Details not found")
    return godown_service.update(db, db_obj=db_godown, obj_in=godown)

# --- Stock Items Details ---
@router.get("/get_stock_items_details", response_model=List[schemas.StockItemsDetails], tags=["Stock Items Details"])
def get_stock_items_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    stock_item_name: Optional[str] = None,
):
    if stock_item_name:
        return db.query(stock_item_service.repository.model).filter(
            stock_item_service.repository.model.stock_item_name.ilike(f"%{stock_item_name}%")
        ).all()
    return stock_item_service.get_multi(db)

@router.get("/get_stock_items_details/{stock_item_id}", response_model=schemas.StockItemsDetails, tags=["Stock Items Details"])
def get_stock_item_detail(stock_item_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    item = stock_item_service.get(db, id=stock_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Stock Item not found")
    return item

@router.post("/create_stock_items_details", response_model=schemas.StockItemsDetails, tags=["Stock Items Details"])
def create_stock_items_details(item: schemas.StockItemsCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return stock_item_service.create(db, obj_in=item)

@router.put("/update_stock_items_details/{stock_item_id}", response_model=schemas.StockItemsDetails, tags=["Stock Items Details"])
def update_stock_items_details(stock_item_id: int, item: schemas.StockItemsUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_item = stock_item_service.get(db, id=stock_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Stock Item not found")
    return stock_item_service.update(db, db_obj=db_item, obj_in=item)

# --- Packaging Details ---
@router.get("/get_packaging_details", response_model=List[schemas.PackagingDetails], tags=["Packaging Details"])
def get_packaging_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    packaging_name: Optional[str] = None,
):
    if packaging_name:
        return db.query(packaging_service.repository.model).filter(
            packaging_service.repository.model.packaging_name.ilike(f"%{packaging_name}%")
        ).all()
    return packaging_service.get_multi(db)

@router.get("/get_packaging_details/{packaging_id}", response_model=schemas.PackagingDetails, tags=["Packaging Details"])
def get_packaging_detail(packaging_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    packaging = packaging_service.get(db, id=packaging_id)
    if not packaging:
        raise HTTPException(status_code=404, detail="Packaging Details not found")
    return packaging

@router.post("/create_packaging_details", response_model=schemas.PackagingDetails, tags=["Packaging Details"])
def create_packaging_details(packaging: schemas.PackagingCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return packaging_service.create(db, obj_in=packaging)

@router.put("/update_packaging_details/{packaging_id}", response_model=schemas.PackagingDetails, tags=["Packaging Details"])
def update_packaging_details(packaging_id: int, packaging: schemas.PackagingUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_packaging = packaging_service.get(db, id=packaging_id)
    if not db_packaging:
        raise HTTPException(status_code=404, detail="Packaging Details not found")
    return packaging_service.update(db, db_obj=db_packaging, obj_in=packaging)

# --- Weight Bridge Operator Details ---
@router.get("/get_weight_bridge_operator_details", response_model=List[schemas.WeightBridgeOperator], tags=["Weight Bridge Operator Details"])
def get_wb_operator_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    operator_name: Optional[str] = None,
):
    if operator_name:
        return db.query(weight_bridge_operator_service.repository.model).filter(
            weight_bridge_operator_service.repository.model.operator_name.ilike(f"%{operator_name}%")
        ).all()
    return weight_bridge_operator_service.get_multi(db)

@router.get("/get_weight_bridge_operator_details/{operator_id}", response_model=schemas.WeightBridgeOperator, tags=["Weight Bridge Operator Details"])
def get_wb_operator_detail(operator_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    operator = weight_bridge_operator_service.get(db, id=operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Weight Bridge Operator not found")
    return operator

@router.post("/create_weight_bridge_operator_details", response_model=schemas.WeightBridgeOperator, tags=["Weight Bridge Operator Details"])
def create_wb_operator_details(operator: schemas.WeightBridgeOperatorCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return weight_bridge_operator_service.create(db, obj_in=operator)

@router.put("/update_weight_bridge_operator_details/{operator_id}", response_model=schemas.WeightBridgeOperator, tags=["Weight Bridge Operator Details"])
def update_wb_operator_details(operator_id: int, operator: schemas.WeightBridgeOperatorUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_operator = weight_bridge_operator_service.get(db, id=operator_id)
    if not db_operator:
        raise HTTPException(status_code=404, detail="Weight Bridge Operator not found")
    return weight_bridge_operator_service.update(db, db_obj=db_operator, obj_in=operator)

@router.delete("/delete_weight_bridge_operator_details/{operator_id}", tags=["Weight Bridge Operator Details"])
def delete_wb_operator_details(operator_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_operator = weight_bridge_operator_service.get(db, id=operator_id)
    if not db_operator:
        raise HTTPException(status_code=404, detail="Weight Bridge Operator not found")
    weight_bridge_operator_service.delete(db, id=operator_id)
    return {"detail": "Weight Bridge Operator deleted successfully"}
