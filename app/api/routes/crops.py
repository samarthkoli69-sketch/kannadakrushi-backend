from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.crop import Crop
from app.schemas.crop import CropCreate


router = APIRouter()


@router.post("/")
def create_crop(
    data: CropCreate,
    db: Session = Depends(get_db)
):
    crop = Crop(**data.model_dump())

    db.add(crop)
    db.commit()
    db.refresh(crop)

    return {
        "success": True,
        "crop_id": crop.id,
        "message": "Crop added successfully"
    }


@router.get("/field/{field_id}")
def get_field_crops(
    field_id: int,
    db: Session = Depends(get_db)
):
    crops = db.query(Crop).filter(
        Crop.field_id == field_id
    ).all()

    return crops