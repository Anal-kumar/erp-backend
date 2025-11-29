from typing import Any, Generic, List, Optional, TypeVar
from sqlalchemy.orm import Session
from app.core.repository import BaseRepository, ModelType, CreateSchemaType, UpdateSchemaType

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return self.repository.get(db, id)

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        return self.repository.create(db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        return self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    def delete(self, db: Session, *, id: int) -> ModelType:
        return self.repository.delete(db, id=id)
