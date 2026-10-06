from datetime import datetime

from pydantic import BaseModel, Field as PydanticField


class FieldCreate(BaseModel):
    farm_id: int

    name: str

    survey_number: str | None = None

    area_acres: float | None = PydanticField(
        default=None,
        gt=0
    )

    latitude: float | None = PydanticField(
        default=None,
        ge=-90,
        le=90
    )

    longitude: float | None = PydanticField(
        default=None,
        ge=-180,
        le=180
    )

    village: str | None = None

    taluk: str | None = None

    district: str | None = None

    state: str = "Karnataka"

    boundary_geojson: dict | None = None

    satellite_monitoring_enabled: bool = True


class FieldResponse(BaseModel):
    id: int
    farm_id: int
    name: str
    survey_number: str | None
    area_acres: float | None
    latitude: float | None
    longitude: float | None
    village: str | None
    taluk: str | None
    district: str | None
    state: str
    boundary_geojson: dict | None
    satellite_monitoring_enabled: bool
    last_satellite_check: datetime | None
    latest_ndvi: float | None
    latest_satellite_status: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }