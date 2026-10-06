from pydantic import BaseModel


class AIChatRequest(BaseModel):
    user_id: int
    farm_id: int | None = None
    field_id: int | None = None
    language: str = "kn"
    message: str


class AIChatResponse(BaseModel):
    success: bool
    language: str
    response: str
    intent: str | None = None
    confidence: float | None = None
    sources: list[str] = []
    requires_human_review: bool = False