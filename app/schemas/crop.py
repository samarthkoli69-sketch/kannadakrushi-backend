from datetime import date

from pydantic import BaseModel


class CropCreate(BaseModel):
    field_id: int
    crop_name: str
    variety: str | None = None
    season: str | None = None
    growth_stage: str | None = None
    sowing_date: date | None = None
    expected_harvest_date: date | None = None