from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.service import BaseService
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate
from app.modules.users.repository import user_repository
from app.core.security import hash_password

class UserService(BaseService[User, UserCreate, UserUpdate]):
    def get_by_login_id(self, db: Session, user_login_id: str) -> Optional[User]:
        return self.repository.get_by_login_id(db, user_login_id=user_login_id)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in.password = hash_password(obj_in.password)
        return super().create(db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            hashed_password = hash_password(update_data["password"])
            update_data["password"] = hashed_password
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_all_except_superadmin(self, db: Session) -> List[User]:
        return db.query(self.repository.model).filter(
            self.repository.model.user_login_id != "superadmin",
            self.repository.model.user_role != "superadmin"
        ).all()

user_service = UserService(user_repository)
