from typing import List, Optional, Any
from sqlalchemy.orm import Session, joinedload
from app.core.repository import BaseRepository
from app.modules.production.models import (
    BatchOperator, Clerks, Batch, SteamOn, SteamOff, Drainage, Immerse,
    MillingAnalysis, SortingAnalysis, CrossVerification, LotDetails
)
from app.modules.production.schemas import (
    BatchOperatorCreate, BatchOperatorUpdate,
    CreateClerk, UpdateClerk,
    CreateBatch, UpdateBatch,
    CreateSteamOn, UpdateSteamOn,
    CreateSteamOff, UpdateSteamOff,
    CreateDrainage, UpdateDrainage,
    CreateImmerse, UpdateImmerse,
    CreateMillingAnalysis, UpdateMillingAnalysis,
    CreateSortingAnalysis, UpdateSortingAnalysis,
    CreateCrossVerification, UpdateCrossVerification,
    CreateLot, UpdateLot
)
from app.modules.users.models import User

class BatchOperatorRepository(BaseRepository[BatchOperator, BatchOperatorCreate, BatchOperatorUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[BatchOperator]:
        return db.query(self.model).options(joinedload(BatchOperator.users).load_only(User.user_login_id)).offset(skip).limit(limit).all()

class ClerkRepository(BaseRepository[Clerks, CreateClerk, UpdateClerk]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Clerks]:
        return db.query(self.model).options(joinedload(Clerks.users).load_only(User.user_login_id)).offset(skip).limit(limit).all()

class BatchRepository(BaseRepository[Batch, CreateBatch, UpdateBatch]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Batch]:
        return db.query(self.model).options(
            joinedload(Batch.stock_items),
            joinedload(Batch.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, batch_name: str) -> Optional[Batch]:
        return db.query(self.model).filter(self.model.batch_name == batch_name).first()

class SteamOnRepository(BaseRepository[SteamOn, CreateSteamOn, UpdateSteamOn]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SteamOn]:
        return db.query(self.model).options(
            joinedload(SteamOn.batch),
            joinedload(SteamOn.first_batch_operator),
            joinedload(SteamOn.second_batch_operator),
            joinedload(SteamOn.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

class SteamOffRepository(BaseRepository[SteamOff, CreateSteamOff, UpdateSteamOff]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SteamOff]:
        return db.query(self.model).options(
            joinedload(SteamOff.batch),
            joinedload(SteamOff.first_batch_operator),
            joinedload(SteamOff.second_batch_operator),
            joinedload(SteamOff.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

class DrainageRepository(BaseRepository[Drainage, CreateDrainage, UpdateDrainage]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Drainage]:
        return db.query(self.model).options(
            joinedload(Drainage.batch),
            joinedload(Drainage.first_batch_operator),
            joinedload(Drainage.second_batch_operator),
            joinedload(Drainage.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

class ImmerseRepository(BaseRepository[Immerse, CreateImmerse, UpdateImmerse]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Immerse]:
        return db.query(self.model).options(
            joinedload(Immerse.batch),
            joinedload(Immerse.first_batch_operator),
            joinedload(Immerse.second_batch_operator),
            joinedload(Immerse.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

class MillingAnalysisRepository(BaseRepository[MillingAnalysis, CreateMillingAnalysis, UpdateMillingAnalysis]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[MillingAnalysis]:
        return db.query(self.model).options(
            joinedload(MillingAnalysis.batch),
            joinedload(MillingAnalysis.analyzer_clerk),
            joinedload(MillingAnalysis.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

class SortingAnalysisRepository(BaseRepository[SortingAnalysis, CreateSortingAnalysis, UpdateSortingAnalysis]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SortingAnalysis]:
        return db.query(self.model).options(
            joinedload(SortingAnalysis.batch),
            joinedload(SortingAnalysis.analyzer_clerk),
            joinedload(SortingAnalysis.checker_clerk),
            joinedload(SortingAnalysis.verifier_clerk),
            joinedload(SortingAnalysis.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

class CrossVerificationRepository(BaseRepository[CrossVerification, CreateCrossVerification, UpdateCrossVerification]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[CrossVerification]:
        return db.query(self.model).options(
            joinedload(CrossVerification.batch),
            joinedload(CrossVerification.checker_clerk),
            joinedload(CrossVerification.verifier_clerk),
            joinedload(CrossVerification.approver_clerk),
            joinedload(CrossVerification.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

class LotDetailsRepository(BaseRepository[LotDetails, CreateLot, UpdateLot]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[LotDetails]:
        return db.query(self.model).options(
            joinedload(LotDetails.checker_clerk),
            joinedload(LotDetails.verifier_clerk),
            joinedload(LotDetails.users).load_only(User.user_login_id)
        ).offset(skip).limit(limit).all()

batch_operator_repository = BatchOperatorRepository(BatchOperator)
clerk_repository = ClerkRepository(Clerks)
batch_repository = BatchRepository(Batch)
steam_on_repository = SteamOnRepository(SteamOn)
steam_off_repository = SteamOffRepository(SteamOff)
drainage_repository = DrainageRepository(Drainage)
immerse_repository = ImmerseRepository(Immerse)
milling_analysis_repository = MillingAnalysisRepository(MillingAnalysis)
sorting_analysis_repository = SortingAnalysisRepository(SortingAnalysis)
cross_verification_repository = CrossVerificationRepository(CrossVerification)
lot_details_repository = LotDetailsRepository(LotDetails)
