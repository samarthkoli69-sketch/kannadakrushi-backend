from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.farm import Farm
from app.schemas.farm import FarmCreate, FarmResponse


router = APIRouter()


@router.post("/", response_model=FarmResponse)
def create_farm(
    data: FarmCreate,
    db: Session = Depends(get_db)
):
    farm = Farm(
        name=data.name,
        owner_id=data.owner_id,
        village=data.village,
        taluk=data.taluk,
        district=data.district,
        state=data.state,
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return farm


@router.get("/owner/{owner_id}", response_model=list[FarmResponse])
def get_owner_farms(
    owner_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Farm).filter(
        Farm.owner_id == owner_id
    ).all()


@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(
    farm_id: int,
    db: Session = Depends(get_db)
):
    farm = db.query(Farm).filter(
        Farm.id == farm_id
    ).first()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    return farm