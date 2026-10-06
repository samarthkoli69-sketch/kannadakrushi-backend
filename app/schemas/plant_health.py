from datetime import datetime

from pydantic import BaseModel


class PlantHealthResponse(BaseModel):
    id: int
    field_id: int
    image_path: str
    predicted_issue: str | None
    confidence: float | None
    status: str
    notes: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }