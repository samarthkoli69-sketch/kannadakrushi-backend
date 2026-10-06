from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.field import Field


router = APIRouter()


@router.get("/fields/{field_id}/status")
def satellite_status(
    field_id: int,
    db: Session = Depends(get_db)
):
    field = db.query(Field).filter(
        Field.id == field_id
    ).first()

    if not field:
        raise HTTPException(
            status_code=404,
            detail="Field not found"
        )

    return {
        "success": True,
        "field_id": field.id,
        "survey_number": field.survey_number,
        "latitude": field.latitude,
        "longitude": field.longitude,
        "monitoring_enabled": field.satellite_monitoring_enabled,
        "last_check": field.last_satellite_check,
        "latest_ndvi": field.latest_ndvi,
        "status": field.latest_satellite_status,
        "message": "Satellite data provider integration pending"
    }