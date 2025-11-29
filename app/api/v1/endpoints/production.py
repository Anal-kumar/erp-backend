from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.core.security import get_current_user
from typing import List, Optional
import app.models.production as models
import app.modules.users.models as user_models
import app.modules.master_data.models as master_models
import app.schemas.production as schemas
import app.modules.users.schemas as user_schemas

router = APIRouter()

# ============================================================
@router.post("/create_batch_operator", response_model=schemas.BatchOperatorResponse)
def create_batch_operator(
    operator: schemas.BatchOperatorCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    try:
        new_operator = models.BatchOperator(**operator.model_dump())
        db.add(new_operator)
        db.commit()
        db.refresh(new_operator)
        return new_operator
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_batch_operators", response_model=List[schemas.BatchOperatorResponse])
def get_batch_operators(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.BatchOperator).options(joinedload(models.BatchOperator.users).load_only(user_models.User.user_login_id)).all()

@router.put("/update_batch_operator/{operator_id}", response_model=schemas.BatchOperatorResponse)
def update_batch_operator(
    operator_id: int, operator: schemas.BatchOperatorUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    db_operator = db.query(models.BatchOperator).filter(models.BatchOperator.id == operator_id).first()
    if not db_operator:
        raise HTTPException(status_code=404, detail="Batch Operator not found")
    
    for key, value in operator.model_dump().items():
        setattr(db_operator, key, value)
    
    db.commit()
    db.refresh(db_operator)
    return db_operator

# ============================================================
# Clerks
# ============================================================
@router.post("/create_clerk", response_model=schemas.ClerkResponse)
def create_clerk(
    clerk: schemas.CreateClerk, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    try:
        new_clerk = models.Clerks(**clerk.model_dump())
        db.add(new_clerk)
        db.commit()
        db.refresh(new_clerk)
        return new_clerk
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_clerks", response_model=List[schemas.ClerkResponse])
def get_clerks(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.Clerks).options(joinedload(models.Clerks.users).load_only(user_models.User.user_login_id)).all()

@router.put("/update_clerk/{clerk_id}", response_model=schemas.ClerkResponse)
def update_clerk(
    clerk_id: int, clerk: schemas.UpdateClerk, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    db_clerk = db.query(models.Clerks).filter(models.Clerks.id == clerk_id).first()
    if not db_clerk:
        raise HTTPException(status_code=404, detail="Clerk not found")
    
    for key, value in clerk.model_dump().items():
        setattr(db_clerk, key, value)
    
    db.commit()
    db.refresh(db_clerk)
    return db_clerk

# ============================================================
# Batch
# ============================================================
@router.post("/create_batch", response_model=schemas.BatchResponse)
def create_batch(batch: schemas.CreateBatch, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_stock_item = db.query(master_models.StockItems).filter(master_models.StockItems.stock_item_name == batch.stock_item_name).first()
    if not db_stock_item:
        raise HTTPException(status_code=404, detail="Stock Item not found")

    db_batch = models.Batch(
        batch_name=batch.batch_name,
        batch_date=batch.batch_date,
        pot_number=batch.pot_number,
        stock_item_id=db_stock_item.id,
        user_login_id=batch.user_login_id
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

@router.get("/get_all_batches", response_model=List[schemas.BatchResponse])
def get_batches(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    batches = db.query(models.Batch).options(
        joinedload(models.Batch.stock_items),
        joinedload(models.Batch.users).load_only(user_models.User.user_login_id)
    ).all()
    return batches

@router.put("/update_batch/{batch_id}", response_model=schemas.BatchResponse)
def update_batch(batch_id: int, batch: schemas.UpdateBatch, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if not db_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    db_batch.batch_name = batch.batch_name
    db_batch.batch_date = batch.batch_date
    db_batch.pot_number = batch.pot_number

    # Get Stock Item ID
    db_stock_item = db.query(master_models.StockItems).filter(master_models.StockItems.stock_item_name == batch.stock_item_name).first()
    if not db_stock_item:
        raise HTTPException(status_code=404, detail="Stock Item not found")
    db_batch.stock_item_id = db_stock_item.id

    db_batch.user_login_id = batch.user_login_id
    db.commit()
    db.refresh(db_batch)
    return db_batch

# ============================================================
# Steam On
# ============================================================
@router.post("/create_steam_on", response_model=schemas.SteamOnResponse)
def create_steam_on(steam_on: schemas.CreateSteamOn, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.batch_name == steam_on.batch_name).first()
    if not db_batch:
         raise HTTPException(status_code=404, detail="Batch not found")
    
    first_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == steam_on.first_batch_operator).first()
    second_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == steam_on.second_batch_operator).first()

    new_steam_on = models.SteamOn(
        batch_id=db_batch.id,
        steam_on_date=steam_on.steam_on_date,
        steam_on_time=steam_on.steam_on_time,
        first_batch_operator_id=first_op.id if first_op else None,
        second_batch_operator_id=second_op.id if second_op else None,
        user_login_id=steam_on.user_login_id
    )
    db.add(new_steam_on)
    db.commit()
    db.refresh(new_steam_on)
    return new_steam_on

@router.get("/get_steam_on_details", response_model=List[schemas.SteamOnResponse])
def get_steam_on(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.SteamOn).options(
        joinedload(models.SteamOn.batch),
        joinedload(models.SteamOn.first_batch_operator),
        joinedload(models.SteamOn.second_batch_operator),
        joinedload(models.SteamOn.users).load_only(user_models.User.user_login_id)
    ).all()

# ============================================================
# Steam Off
# ============================================================
@router.post("/create_steam_off", response_model=schemas.SteamOffResponse)
def create_steam_off(steam_off: schemas.CreateSteamOff, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.batch_name == steam_off.batch_name).first()
    if not db_batch:
         raise HTTPException(status_code=404, detail="Batch not found")
    
    first_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == steam_off.first_batch_operator).first()
    second_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == steam_off.second_batch_operator).first()

    new_steam_off = models.SteamOff(
        batch_id=db_batch.id,
        steam_off_date=steam_off.steam_off_date,
        steam_off_time=steam_off.steam_off_time,
        first_batch_operator_id=first_op.id if first_op else None,
        second_batch_operator_id=second_op.id if second_op else None,
        user_login_id=steam_off.user_login_id
    )
    db.add(new_steam_off)
    db.commit()
    db.refresh(new_steam_off)
    return new_steam_off

@router.get("/get_steam_off_details", response_model=List[schemas.SteamOffResponse])
def get_steam_off(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.SteamOff).options(
        joinedload(models.SteamOff.batch),
        joinedload(models.SteamOff.first_batch_operator),
        joinedload(models.SteamOff.second_batch_operator),
        joinedload(models.SteamOff.users).load_only(user_models.User.user_login_id)
    ).all()

# ============================================================
# Drainage
# ============================================================
@router.post("/create_drainage", response_model=schemas.DrainageResponse)
def create_drainage(drainage: schemas.CreateDrainage, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.batch_name == drainage.batch_name).first()
    if not db_batch:
         raise HTTPException(status_code=404, detail="Batch not found")
    
    first_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == drainage.first_batch_operator).first()
    second_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == drainage.second_batch_operator).first()

    new_drainage = models.Drainage(
        batch_id=db_batch.id,
        drainage_date=drainage.drainage_date,
        drainage_time=drainage.drainage_time,
        first_batch_operator_id=first_op.id if first_op else None,
        second_batch_operator_id=second_op.id if second_op else None,
        user_login_id=drainage.user_login_id
    )
    db.add(new_drainage)
    db.commit()
    db.refresh(new_drainage)
    return new_drainage

@router.get("/get_drainage_details", response_model=List[schemas.DrainageResponse])
def get_drainage(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.Drainage).options(
        joinedload(models.Drainage.batch),
        joinedload(models.Drainage.first_batch_operator),
        joinedload(models.Drainage.second_batch_operator),
        joinedload(models.Drainage.users).load_only(user_models.User.user_login_id)
    ).all()


# ============================================================
# Immerse
# ============================================================
@router.post("/create_immerse", response_model=schemas.ImmerseResponse)
def create_immerse(immerse: schemas.CreateImmerse, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.batch_name == immerse.batch_name).first()
    if not db_batch:
         raise HTTPException(status_code=404, detail="Batch not found")
    
    first_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == immerse.first_batch_operator).first()
    second_op = db.query(models.BatchOperator).filter(models.BatchOperator.operator_name == immerse.second_batch_operator).first()

    new_immerse = models.Immerse(
        batch_id=db_batch.id,
        immersion_date=immerse.immersion_date,
        immersion_time=immerse.immersion_time,
        first_batch_operator_id=first_op.id if first_op else None,
        second_batch_operator_id=second_op.id if second_op else None,
        user_login_id=immerse.user_login_id
    )
    db.add(new_immerse)
    db.commit()
    db.refresh(new_immerse)
    return new_immerse

@router.get("/get_immerse_details", response_model=List[schemas.ImmerseResponse])
def get_immerse(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.Immerse).options(
        joinedload(models.Immerse.batch),
        joinedload(models.Immerse.first_batch_operator),
        joinedload(models.Immerse.second_batch_operator),
        joinedload(models.Immerse.users).load_only(user_models.User.user_login_id)
    ).all()

# ============================================================
# Milling Analysis
# ============================================================
@router.post("/create_milling_analysis", response_model=schemas.MillingAnalysisResponse)
def create_milling_analysis(analysis: schemas.CreateMillingAnalysis, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.batch_name == analysis.batch_name).first()
    if not db_batch:
         raise HTTPException(status_code=404, detail="Batch not found")
    
    clerk = db.query(models.Clerks).filter(models.Clerks.clerk_name == analysis.analyzer_clerk_name).first()

    new_analysis = models.MillingAnalysis(
        batch_id=db_batch.id,
        analyzer_clerk_id=clerk.id if clerk else None,
        milling_rice_moisture_percent=analysis.milling_rice_moisture_percent,
        milling_broken_percent=analysis.milling_broken_percent,
        milling_discolor_percent=analysis.milling_discolor_percent,
        milling_damaged_percent=analysis.milling_damaged_percent,
        milling_output_porridge_30sec=analysis.milling_output_porridge_30sec,
        milling_output_final_polisher_30sec=analysis.milling_output_final_polisher_30sec,
        user_login_id=analysis.user_login_id
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis

@router.get("/get_milling_analysis_details", response_model=List[schemas.MillingAnalysisResponse])
def get_milling_analysis(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.MillingAnalysis).options(
        joinedload(models.MillingAnalysis.batch),
        joinedload(models.MillingAnalysis.analyzer_clerk),
        joinedload(models.MillingAnalysis.users).load_only(user_models.User.user_login_id)
    ).all()

# ============================================================
# Sorting Analysis
# ============================================================
@router.post("/create_sorting_analysis", response_model=schemas.SortingAnalysisResponse)
def create_sorting_analysis(analysis: schemas.CreateSortingAnalysis, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.batch_name == analysis.batch_name).first()
    if not db_batch:
         raise HTTPException(status_code=404, detail="Batch not found")
    
    analyzer = db.query(models.Clerks).filter(models.Clerks.clerk_name == analysis.analyzer_clerk_name).first()
    checker = db.query(models.Clerks).filter(models.Clerks.clerk_name == analysis.checker_clerk_name).first()
    verifier = db.query(models.Clerks).filter(models.Clerks.clerk_name == analysis.verifier_clerk_name).first()

    new_analysis = models.SortingAnalysis(
        batch_id=db_batch.id,
        analyzer_clerk_id=analyzer.id if analyzer else None,
        sorted_rice_moisture_percent=analysis.sorted_rice_moisture_percent,
        sorted_broken_percent=analysis.sorted_broken_percent,
        sorted_discolor_percent=analysis.sorted_discolor_percent,
        sorted_damaged_percent=analysis.sorted_damaged_percent,
        rejection_rice_percent=analysis.rejection_rice_percent,
        sorting_output_30sec=analysis.sorting_output_30sec,
        rejection_output_30sec=analysis.rejection_output_30sec,
        checker_clerk_id=checker.id if checker else None,
        checking_date=analysis.checking_date,
        checking_time=analysis.checking_time,
        verifier_clerk_id=verifier.id if verifier else None,
        verifying_date=analysis.verifying_date,
        verifying_time=analysis.verifying_time,
        user_login_id=analysis.user_login_id
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis

@router.get("/get_sorting_analysis_details", response_model=List[schemas.SortingAnalysisResponse])
def get_sorting_analysis(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.SortingAnalysis).options(
        joinedload(models.SortingAnalysis.batch),
        joinedload(models.SortingAnalysis.analyzer_clerk),
        joinedload(models.SortingAnalysis.checker_clerk),
        joinedload(models.SortingAnalysis.verifier_clerk),
        joinedload(models.SortingAnalysis.users).load_only(user_models.User.user_login_id)
    ).all()

# ============================================================
# Cross Verification
# ============================================================
@router.post("/create_cross_verification", response_model=schemas.CrossVerificationResponse)
def create_cross_verification(verification: schemas.CreateCrossVerification, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_batch = db.query(models.Batch).filter(models.Batch.batch_name == verification.batch_name).first()
    if not db_batch:
         raise HTTPException(status_code=404, detail="Batch not found")
    
    checker = db.query(models.Clerks).filter(models.Clerks.clerk_name == verification.checker_clerk_name).first()
    verifier = db.query(models.Clerks).filter(models.Clerks.clerk_name == verification.verifier_clerk_name).first()
    approver = db.query(models.Clerks).filter(models.Clerks.clerk_name == verification.approver_clerk_name).first()

    new_verification = models.CrossVerification(
        batch_id=db_batch.id,
        checker_clerk_id=checker.id if checker else None,
        checking_date=verification.checking_date,
        checking_time=verification.checking_time,
        verifier_clerk_id=verifier.id if verifier else None,
        verifying_date=verification.verifying_date,
        verifying_time=verification.verifying_time,
        paddy_moisture_percent=verification.paddy_moisture_percent,
        approver_clerk_id=approver.id if approver else None,
        user_login_id=verification.user_login_id
    )
    db.add(new_verification)
    db.commit()
    db.refresh(new_verification)
    return new_verification

@router.get("/get_cross_verification_details", response_model=List[schemas.CrossVerificationResponse])
def get_cross_verification(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.CrossVerification).options(
        joinedload(models.CrossVerification.batch),
        joinedload(models.CrossVerification.checker_clerk),
        joinedload(models.CrossVerification.verifier_clerk),
        joinedload(models.CrossVerification.approver_clerk),
        joinedload(models.CrossVerification.users).load_only(user_models.User.user_login_id)
    ).all()

# ============================================================
# Lot Details
# ============================================================
@router.post("/create_lot_details", response_model=schemas.LotDetailsResponse)
def create_lot_details(lot: schemas.CreateLot, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    checker = db.query(models.Clerks).filter(models.Clerks.clerk_name == lot.checker_clerk).first()
    verifier = db.query(models.Clerks).filter(models.Clerks.clerk_name == lot.verifier_clerk).first()

    new_lot = models.LotDetails(
        lot_number=lot.lot_number,
        lot_moisture_percent=lot.lot_moisture_percent,
        lot_broken_percent=lot.lot_broken_percent,
        lot_discolor_percent=lot.lot_discolor_percent,
        lot_damaged_percent=lot.lot_damaged_percent,
        lot_lower_grain_percent=lot.lot_lower_grain_percent,
        lot_chalky_percent=lot.lot_chalky_percent,
        lot_frk_percent=lot.lot_frk_percent,
        lot_other_percent=lot.lot_other_percent,
        checker_clerk_id=checker.id if checker else None,
        checking_date=lot.checking_date,
        checking_time=lot.checking_time,
        verifier_clerk_id=verifier.id if verifier else None,
        verifying_date=lot.verifying_date,
        verifying_time=lot.verifying_time,
        user_login_id=lot.user_login_id
    )
    db.add(new_lot)
    db.commit()
    db.refresh(new_lot)
    return new_lot

@router.get("/get_lot_details", response_model=List[schemas.LotDetailsResponse])
def get_lot_details(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.LotDetails).options(
        joinedload(models.LotDetails.checker_clerk),
        joinedload(models.LotDetails.verifier_clerk),
        joinedload(models.LotDetails.users).load_only(user_models.User.user_login_id)
    ).all()
