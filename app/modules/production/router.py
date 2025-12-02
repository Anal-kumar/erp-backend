from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.security import get_current_user
from app.modules.production.service import production_service
from app.modules.production.schemas import (
    BatchOperatorCreate, BatchOperatorUpdate, BatchOperatorResponse,
    CreateClerk, UpdateClerk, ClerkResponse,
    CreateBatch, UpdateBatch, BatchResponse,
    CreateSteamOn, UpdateSteamOn, SteamOnResponse,
    CreateSteamOff, UpdateSteamOff, SteamOffResponse,
    CreateDrainage, UpdateDrainage, DrainageResponse,
    CreateImmerse, UpdateImmerse, ImmerseResponse,
    CreateMillingAnalysis, UpdateMillingAnalysis, MillingAnalysisResponse,
    CreateSortingAnalysis, UpdateSortingAnalysis, SortingAnalysisResponse,
    CreateCrossVerification, UpdateCrossVerification, CrossVerificationResponse,
    CreateLot, UpdateLot, LotDetailsResponse
)

router = APIRouter()

# --- Batch Operator ---
@router.get("/get_batch_operators", response_model=List[BatchOperatorResponse])
def get_batch_operators(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_batch_operators(db)

@router.post("/create_batch_operator", response_model=BatchOperatorResponse)
def create_batch_operator(operator: BatchOperatorCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_batch_operator(db, operator)

@router.put("/update_batch_operator/{id}", response_model=BatchOperatorResponse)
def update_batch_operator(id: int, operator: BatchOperatorUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.update_batch_operator(db, id, operator)

# --- Clerks ---
@router.get("/get_clerks", response_model=List[ClerkResponse])
def get_clerks(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_clerks(db)

@router.post("/create_clerk", response_model=ClerkResponse)
def create_clerk(clerk: CreateClerk, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_clerk(db, clerk)

@router.put("/update_clerk/{id}", response_model=ClerkResponse)
def update_clerk(id: int, clerk: UpdateClerk, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.update_clerk(db, id, clerk)

# --- Batch ---
@router.get("/get_all_batches", response_model=List[BatchResponse])
def get_batches(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_batches(db)

@router.post("/create_batch", response_model=BatchResponse)
def create_batch(batch: CreateBatch, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_batch(db, batch)

@router.put("/update_batch/{id}", response_model=BatchResponse)
def update_batch(id: int, batch: UpdateBatch, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.update_batch(db, id, batch)

# --- Steam On ---
@router.get("/get_steam_on_details", response_model=List[SteamOnResponse])
def get_steam_on(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_steam_on(db)

@router.post("/create_steam_on", response_model=SteamOnResponse)
def create_steam_on(steam_on: CreateSteamOn, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_steam_on(db, steam_on)

# --- Steam Off ---
@router.get("/get_steam_off_details", response_model=List[SteamOffResponse])
def get_steam_off(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_steam_off(db)

@router.post("/create_steam_off", response_model=SteamOffResponse)
def create_steam_off(steam_off: CreateSteamOff, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_steam_off(db, steam_off)

# --- Drainage ---
@router.get("/get_drainage_details", response_model=List[DrainageResponse])
def get_drainage(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_drainage(db)

@router.post("/create_drainage", response_model=DrainageResponse)
def create_drainage(drainage: CreateDrainage, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_drainage(db, drainage)

# --- Immerse ---
@router.get("/get_immerse_details", response_model=List[ImmerseResponse])
def get_immerse(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_immerse(db)

@router.post("/create_immerse", response_model=ImmerseResponse)
def create_immerse(immerse: CreateImmerse, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_immerse(db, immerse)

# --- Milling Analysis ---
@router.get("/get_milling_analysis_details", response_model=List[MillingAnalysisResponse])
def get_milling_analysis(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_milling_analysis(db)

@router.post("/create_milling_analysis", response_model=MillingAnalysisResponse)
def create_milling_analysis(analysis: CreateMillingAnalysis, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_milling_analysis(db, analysis)

# --- Sorting Analysis ---
@router.get("/get_sorting_analysis_details", response_model=List[SortingAnalysisResponse])
def get_sorting_analysis(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_sorting_analysis(db)

@router.post("/create_sorting_analysis", response_model=SortingAnalysisResponse)
def create_sorting_analysis(analysis: CreateSortingAnalysis, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_sorting_analysis(db, analysis)

# --- Cross Verification ---
@router.get("/get_cross_verification_details", response_model=List[CrossVerificationResponse])
def get_cross_verification(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_cross_verification(db)

@router.post("/create_cross_verification", response_model=CrossVerificationResponse)
def create_cross_verification(verification: CreateCrossVerification, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_cross_verification(db, verification)

# --- Lot Details ---
@router.get("/get_lot_details", response_model=List[LotDetailsResponse])
def get_lot_details(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.get_lot_details(db)

@router.post("/create_lot_details", response_model=LotDetailsResponse)
def create_lot_details(lot: CreateLot, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return production_service.create_lot_details(db, lot)
