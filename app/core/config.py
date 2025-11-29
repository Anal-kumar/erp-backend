

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Rice Mill ERP"
    VERSION: str = os.getenv("VERSION", "v1")
    API_V1_STR: str = f"/api/{VERSION}"
    
    # Database configuration - using static filename
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database/rice_mill.db")
    ENV: str = os.getenv("ENV", "development")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
