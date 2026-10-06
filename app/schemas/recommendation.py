from datetime import datetime

from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: int
    field_id: int
    category: str
    title: str
    message: str
    priority: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }