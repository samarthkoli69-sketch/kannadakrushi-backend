from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.field import Field
from app.schemas.field import FieldCreate, FieldResponse


router = APIRouter()


@router.post("/", response_model=FieldResponse)
def create_field(
    data: FieldCreate,
    db: Session = Depends(get_db)
):
    field = Field(**data.model_dump())

    db.add(field)
    db.commit()
    db.refresh(field)

    return field


@router.get("/farm/{farm_id}", response_model=list[FieldResponse])
def get_farm_fields(
    farm_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Field).filter(
        Field.farm_id == farm_id
    ).all()


@router.get("/{field_id}", response_model=FieldResponse)
def get_field(
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

    return field