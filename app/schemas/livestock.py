from datetime import date, datetime

from pydantic import BaseModel, Field


# ============================================================
# LIVESTOCK
# ============================================================

class LivestockCreate(BaseModel):
    farm_id: int
    animal_tag: str = Field(min_length=1, max_length=100)
    animal_type: str = Field(min_length=1, max_length=50)
    breed: str | None = Field(default=None, max_length=100)
    gender: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = None
    weight: float | None = Field(default=None, gt=0)
    health_status: str = Field(default="healthy", max_length=50)
    photo_url: str | None = Field(default=None, max_length=500)
    notes: str | None = None


class LivestockUpdate(BaseModel):
    animal_tag: str | None = Field(default=None, min_length=1, max_length=100)
    animal_type: str | None = Field(default=None, min_length=1, max_length=50)
    breed: str | None = Field(default=None, max_length=100)
    gender: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = None
    weight: float | None = Field(default=None, gt=0)
    health_status: str | None = Field(default=None, max_length=50)
    photo_url: str | None = Field(default=None, max_length=500)
    notes: str | None = None


class LivestockResponse(BaseModel):
    id: int
    farm_id: int
    animal_tag: str
    animal_type: str
    breed: str | None
    gender: str | None
    date_of_birth: date | None
    weight: float | None
    health_status: str
    photo_url: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# ============================================================
# HEALTH RECORDS
# ============================================================

class LivestockHealthRecordCreate(BaseModel):
    record_date: date | None = None
    health_status: str = Field(min_length=1, max_length=50)
    symptoms: str | None = None
    treatment_notes: str | None = None
    veterinary_notes: str | None = None


class LivestockHealthRecordResponse(BaseModel):
    id: int
    livestock_id: int
    record_date: date
    health_status: str
    symptoms: str | None
    treatment_notes: str | None
    veterinary_notes: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# ============================================================
# VACCINATIONS
# ============================================================

class LivestockVaccinationCreate(BaseModel):
    vaccine_name: str = Field(min_length=1, max_length=150)
    vaccination_date: date
    next_due_date: date | None = None
    notes: str | None = None


class LivestockVaccinationResponse(BaseModel):
    id: int
    livestock_id: int
    vaccine_name: str
    vaccination_date: date
    next_due_date: date | None
    notes: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }