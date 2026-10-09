from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.field import Field

router = APIRouter()

BHUVAN_WMS_URL = "https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms"
BHUVAN_LULC_LAYER = "lulc:KA_LULC50K_1516"


@router.get("/fields/{field_id}")
def get_satellite_data(
    field_id: int,
    db: Session = Depends(get_db),
):
    field = (
        db.query(Field)
        .filter(Field.id == field_id)
        .first()
    )

    if not field:
        raise HTTPException(
            status_code=404,
            detail="Field not found",
        )

    if field.latitude is None or field.longitude is None:
        raise HTTPException(
            status_code=400,
            detail="Field GPS coordinates are required for satellite monitoring",
        )

    return {
        "success": True,
        "source": "ISRO/NRSC Bhuvan",
        "provider": "Bhuvan",
        "field": {
            "id": field.id,
            "farm_id": field.farm_id,
            "name": field.name,
            "latitude": field.latitude,
            "longitude": field.longitude,
            "area_acres": field.area_acres,
            "survey_number": field.survey_number,
            "boundary_geojson": field.boundary_geojson,
        },
        "bhuvan": {
            "wms_url": BHUVAN_WMS_URL,
            "layer": BHUVAN_LULC_LAYER,
            "version": "1.1.1",
            "format": "image/png",
            "crs": "EPSG:4326",
            "dataset": "Karnataka Land Use Land Cover 50K 2015-16",
        },
        "satellite": {
            "monitoring_enabled": field.satellite_monitoring_enabled,
            "latest_ndvi": field.latest_ndvi,
            "last_check": field.last_satellite_check,
            "status": field.latest_satellite_status
            or "Bhuvan monitoring available",
        },
    }


@router.get("/status")
def satellite_status():
    return {
        "success": True,
        "provider": "ISRO/NRSC Bhuvan",
        "status": "available",
        "service": "Bhuvan WMS",
        "wms_url": BHUVAN_WMS_URL,
    }