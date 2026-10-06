from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import engine


router = APIRouter()


@router.get("/health")
def health_check():
    database_status = "disconnected"

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            database_status = "connected"

    except Exception as error:
        database_status = f"error: {str(error)}"

    return {
        "success": True,
        "message": "KannadaKrishi Backend is running",
        "status": "healthy",
        "database": database_status
    }