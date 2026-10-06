from fastapi import APIRouter


router = APIRouter()


@router.get("/field/{field_id}")
def field_weather(field_id: int):
    return {
        "success": True,
        "field_id": field_id,
        "status": "pending",
        "message": "Weather API integration will be connected here."
    }