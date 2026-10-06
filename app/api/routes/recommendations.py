from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.recommendation import Recommendation


router = APIRouter()


@router.get("/")
def get_recommendations(
    field_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Recommendation)

    if field_id:
        query = query.filter(
            Recommendation.field_id == field_id
        )

    return query.order_by(
        Recommendation.created_at.desc()
    ).all()