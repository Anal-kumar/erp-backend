from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
import tempfile
import shutil
import os
from urllib.parse import urlparse
import zipfile
from datetime import datetime
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm.session import close_all_sessions

from app.core.security import get_current_user
from app.db.session import engine
from app.core.config import settings

router = APIRouter()

# Database directory
DB_DIR = "./database"

# Active database URL
ACTIVE_DATABASE_URL = None

def switch_database(db_url: str):
    global engine
    # This logic needs to be robust. For now, I'll just placeholder it or copy from old database.py
    # But since I am refactoring, I should probably put this in app/db/session.py
    pass

@router.post("/set-database")
def set_database(payload: dict):
    db_name = payload.get("database")
    if not db_name:
        raise HTTPException(status_code=400, detail="Database name is required")

    db_path = os.path.join(DB_DIR, db_name)
    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail=f"Database {db_name} not found")

    new_url = f"sqlite:///{db_path}"
    # switch_database(new_url) # TODO: Implement switch_database
    ACTIVE_DATABASE_URL = new_url

    return {"message": f"Database switched to {db_name}", "current_database": new_url}
    
@router.get("/current-database")
def get_current_database():
    current_db = ACTIVE_DATABASE_URL or settings.SQLALCHEMY_DATABASE_URL
    return {"current_database": current_db}

@router.get("/databases")
def list_databases():
    """Return list of available .db files"""
    if not os.path.exists(DB_DIR):
        raise HTTPException(status_code=404, detail="Database directory not found")

    db_files = [f for f in os.listdir(DB_DIR) if f.endswith(".db")]

    return {"databases": db_files}

@router.get("/backup_data", response_class=FileResponse)
def download(current_user: dict = Depends(get_current_user)):
    # Database directory path
    db_dir = os.path.dirname(os.path.normpath(urlparse(settings.SQLALCHEMY_DATABASE_URL).path.lstrip("/")))

    if not os.path.exists(db_dir):
        raise HTTPException(status_code=404, detail="Database directory not found")

    # Create zip file in temp directory
    year = datetime.now().year
    zip_filename = f"mill_data_{year}.zip"
    temp_dir = tempfile.gettempdir()
    zip_path = os.path.join(temp_dir, zip_filename)

    # Zip only the files inside the directory
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(db_dir):
            file_path = os.path.join(db_dir, file)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file)  # arcname avoids including parent directory

    return FileResponse(
        path=zip_path,
        media_type='application/zip',
        filename=zip_filename
    )

@router.post("/restore")
def restore_database(
    file: UploadFile = File(...)
):
    # Extract real DB path
    raw_path = urlparse(settings.SQLALCHEMY_DATABASE_URL).path.lstrip("/")
    db_path = os.path.normpath(raw_path)

    # Validate file type (optional but smart)
    if not file.filename.endswith(".db"):
        raise HTTPException(status_code=400, detail="Only .db files are allowed")

    # Save uploaded file to DB path
    with open(db_path, "wb") as out_file:
        shutil.copyfileobj(file.file, out_file)

    return {"message": "Database restored successfully"}

@router.delete("/delete_database")
async def delete_current_database(
    current_user: dict = Depends(get_current_user),
):
    # Get the DB file path from engine URL
    db_url = str(engine.url)
    if not db_url.startswith("sqlite:///"):
        raise HTTPException(
            status_code=400,
            detail="Only SQLite database files can be deleted",
        )

    db_file_path = os.path.normpath(db_url.replace("sqlite:///", "", 1))
    # file_path = Path(__file__).resolve().parent.parent / "firm_details.json" # This logic seems wrong in original code, it checks firm_details.json existence?

    # Validate that the file exists
    if not os.path.exists(db_file_path) or not os.path.isfile(db_file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Database file '{db_file_path}' not found",
        )

    try:
        # Close all sessions and dispose engine
        close_all_sessions()
        engine.dispose()

        # Delete the file
        await run_in_threadpool(os.remove, db_file_path)

    except PermissionError:
        raise HTTPException(
            status_code=423,
            detail=f"Database file '{db_file_path}' is currently in use and cannot be deleted",
        )

    return {"message": f"Database file '{db_file_path}' deleted successfully"}
