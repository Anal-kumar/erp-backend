from pydantic import BaseModel
from typing import Optional

class Module(BaseModel):
    id: int
    module_name: str
    module_enabled: bool

    class Config:
        from_attributes = True

class ModuleUpdate(BaseModel):
    module_enabled: bool

    class Config:
        from_attributes = True
