from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from typing import List
from app.models.module import ModuleControl
import app.models.module as models
import app.schemas.module as schemas

router = APIRouter()

@router.get("/get_modules")
def get_modules(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    modules = db.query(models.ModuleControl).all()
    return modules

# Get enabled modules
@router.get("/enabled_modules")
def get_enabled_modules(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(models.ModuleControl).filter(
        models.ModuleControl.module_enabled == True,
    ).all()

@router.get("/get_module/{module_id}")
def get_module(module_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    module = db.query(models.ModuleControl).filter(models.ModuleControl.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@router.put("/update_modules/{module_id}")
def update_module(module_id: int, module: schemas.ModuleUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_module = db.query(models.ModuleControl).filter(models.ModuleControl.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    for key, value in module.model_dump().items():
        setattr(db_module, key, value)
    db.commit()
    db.refresh(db_module)
    return db_module
