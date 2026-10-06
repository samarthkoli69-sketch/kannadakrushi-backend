from datetime import datetime

from pydantic import BaseModel


class FarmCreate(BaseModel):
    name: str
    owner_id: int
    village: str | None = None
    taluk: str | None = None
    district: str | None = None
    state: str = "Karnataka"


class FarmResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    village: str | None
    taluk: str | None
    district: str | None
    state: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }