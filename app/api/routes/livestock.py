from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.farm import Farm
from app.models.livestock import Livestock
from app.models.livestock_health_record import LivestockHealthRecord
from app.models.livestock_vaccination import LivestockVaccination
from app.schemas.livestock import (
    LivestockCreate,
    LivestockHealthRecordCreate,
    LivestockHealthRecordResponse,
    LivestockResponse,
    LivestockUpdate,
    LivestockVaccinationCreate,
    LivestockVaccinationResponse,
)

router = APIRouter()


# ============================================================
# LIVESTOCK
# ============================================================

@router.post(
    "",
    response_model=LivestockResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_livestock(
    data: LivestockCreate,
    db: Session = Depends(get_db),
):
    # Check whether farm exists
    farm = db.query(Farm).filter(Farm.id == data.farm_id).first()

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    # Prevent duplicate animal tag inside the same farm
    existing = (
        db.query(Livestock)
        .filter(
            Livestock.farm_id == data.farm_id,
            Livestock.animal_tag == data.animal_tag,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Animal tag already exists in this farm",
        )

    livestock = Livestock(
        farm_id=data.farm_id,
        animal_tag=data.animal_tag,
        animal_type=data.animal_type,
        breed=data.breed,
        gender=data.gender,
        date_of_birth=data.date_of_birth,
        weight=data.weight,
        health_status=data.health_status,
        photo_url=data.photo_url,
        notes=data.notes,
    )

    db.add(livestock)
    db.commit()
    db.refresh(livestock)

    return livestock


@router.get(
    "",
    response_model=list[LivestockResponse],
)
def get_livestock(
    farm_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Livestock)

    if farm_id is not None:
        query = query.filter(Livestock.farm_id == farm_id)

    return query.order_by(Livestock.id.desc()).all()


@router.get(
    "/{livestock_id}",
    response_model=LivestockResponse,
)
def get_livestock_by_id(
    livestock_id: int,
    db: Session = Depends(get_db),
):
    livestock = (
        db.query(Livestock)
        .filter(Livestock.id == livestock_id)
        .first()
    )

    if not livestock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestock not found",
        )

    return livestock


@router.put(
    "/{livestock_id}",
    response_model=LivestockResponse,
)
def update_livestock(
    livestock_id: int,
    data: LivestockUpdate,
    db: Session = Depends(get_db),
):
    livestock = (
        db.query(Livestock)
        .filter(Livestock.id == livestock_id)
        .first()
    )

    if not livestock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestock not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    # Check duplicate tag if tag is being changed
    if "animal_tag" in update_data:
        existing = (
            db.query(Livestock)
            .filter(
                Livestock.farm_id == livestock.farm_id,
                Livestock.animal_tag == update_data["animal_tag"],
                Livestock.id != livestock.id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Animal tag already exists in this farm",
            )

    for field, value in update_data.items():
        setattr(livestock, field, value)

    db.commit()
    db.refresh(livestock)

    return livestock


@router.delete(
    "/{livestock_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_livestock(
    livestock_id: int,
    db: Session = Depends(get_db),
):
    livestock = (
        db.query(Livestock)
        .filter(Livestock.id == livestock_id)
        .first()
    )

    if not livestock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestock not found",
        )

    db.delete(livestock)
    db.commit()

    return None


# ============================================================
# HEALTH RECORDS
# ============================================================

@router.post(
    "/{livestock_id}/health",
    response_model=LivestockHealthRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_health_record(
    livestock_id: int,
    data: LivestockHealthRecordCreate,
    db: Session = Depends(get_db),
):
    livestock = (
        db.query(Livestock)
        .filter(Livestock.id == livestock_id)
        .first()
    )

    if not livestock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestock not found",
        )

    record = LivestockHealthRecord(
        livestock_id=livestock_id,
        health_status=data.health_status,
        symptoms=data.symptoms,
        treatment_notes=data.treatment_notes,
        veterinary_notes=data.veterinary_notes,
    )

    if data.record_date is not None:
        record.record_date = data.record_date

    db.add(record)

    # Keep current animal health status updated
    livestock.health_status = data.health_status

    db.commit()
    db.refresh(record)

    return record


@router.get(
    "/{livestock_id}/health",
    response_model=list[LivestockHealthRecordResponse],
)
def get_health_records(
    livestock_id: int,
    db: Session = Depends(get_db),
):
    livestock = (
        db.query(Livestock)
        .filter(Livestock.id == livestock_id)
        .first()
    )

    if not livestock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestock not found",
        )

    return (
        db.query(LivestockHealthRecord)
        .filter(LivestockHealthRecord.livestock_id == livestock_id)
        .order_by(LivestockHealthRecord.record_date.desc())
        .all()
    )


# ============================================================
# VACCINATIONS
# ============================================================

@router.post(
    "/{livestock_id}/vaccinations",
    response_model=LivestockVaccinationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vaccination(
    livestock_id: int,
    data: LivestockVaccinationCreate,
    db: Session = Depends(get_db),
):
    livestock = (
        db.query(Livestock)
        .filter(Livestock.id == livestock_id)
        .first()
    )

    if not livestock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestock not found",
        )

    vaccination = LivestockVaccination(
        livestock_id=livestock_id,
        vaccine_name=data.vaccine_name,
        vaccination_date=data.vaccination_date,
        next_due_date=data.next_due_date,
        notes=data.notes,
    )

    db.add(vaccination)
    db.commit()
    db.refresh(vaccination)

    return vaccination


@router.get(
    "/{livestock_id}/vaccinations",
    response_model=list[LivestockVaccinationResponse],
)
def get_vaccinations(
    livestock_id: int,
    db: Session = Depends(get_db),
):
    livestock = (
        db.query(Livestock)
        .filter(Livestock.id == livestock_id)
        .first()
    )

    if not livestock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livestock not found",
        )

    return (
        db.query(LivestockVaccination)
        .filter(
            LivestockVaccination.livestock_id == livestock_id
        )
        .order_by(
            LivestockVaccination.vaccination_date.desc()
        )
        .all()
    )