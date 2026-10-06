from datetime import datetime

from pydantic import BaseModel


class IoTReadingCreate(BaseModel):
    device_id: str
    field_id: int

    soil_moisture: float | None = None
    soil_temperature: float | None = None
    soil_ph: float | None = None
    air_temperature: float | None = None
    humidity: float | None = None
    water_level: float | None = None
    rainfall: float | None = None

    recorded_at: datetime | None = None


class SensorResponse(BaseModel):
    id: int
    device_id: str
    field_id: int
    device_type: str
    name: str | None
    is_active: bool
    last_seen: datetime | None

    model_config = {
        "from_attributes": True
    }