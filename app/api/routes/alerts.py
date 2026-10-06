from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.alert import Alert


router = APIRouter()


@router.get("/")
def get_alerts(
    field_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Alert)

    if field_id:
        query = query.filter(
            Alert.field_id == field_id
        )

    return query.order_by(
        Alert.created_at.desc()
    ).all()