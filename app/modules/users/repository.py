from sqlalchemy.orm import Session
from typing import Optional
from app.core.repository import BaseRepository
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_login_id(self, db: Session, *, user_login_id: str) -> Optional[User]:
        return db.query(User).filter(User.user_login_id == user_login_id).first()

user_repository = UserRepository(User)
