from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ModuleControl(Base):
    __tablename__ = "module_control"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_login_id = Column(Integer, ForeignKey("users.id"), index=True)
    module_name = Column(String(30), index=True)
    module_enabled = Column(Boolean, default=False)

    users = relationship("User", back_populates="module_control")
