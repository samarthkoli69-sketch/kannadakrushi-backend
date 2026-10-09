import os

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.farm import Farm
from app.models.field import Field
from app.models.crop import Crop
from app.models.livestock import Livestock
from app.models.alert import Alert
from app.models.recommendation import Recommendation
from app.models.sensor import Sensor
from app.models.sensor_reading import SensorReading
from app.schemas.ai import AIChatRequest

router = APIRouter()

AI_AGENT_URL = os.getenv(
    "AI_AGENT_URL",
    "http://127.0.0.1:9000",
)


def safe_dict(obj, fields):
    if not obj:
        return None

    return {
        field: getattr(obj, field, None)
        for field in fields
    }


@router.post("/chat")
async def chat(
    request: AIChatRequest,
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # 1. USER
    # ---------------------------------------------------------

    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # ---------------------------------------------------------
    # 2. FARM
    # ---------------------------------------------------------

    farm = None

    if request.farm_id:
        farm = db.query(Farm).filter(
            Farm.id == request.farm_id,
            Farm.owner_id == user.id,
        ).first()
    else:
        farm = db.query(Farm).filter(
            Farm.owner_id == user.id
        ).first()

    # ---------------------------------------------------------
    # 3. FIELD
    # ---------------------------------------------------------

    field = None

    if request.field_id:
        field = db.query(Field).filter(
            Field.id == request.field_id,
        ).first()
    elif farm:
        field = db.query(Field).filter(
            Field.farm_id == farm.id
        ).first()

    # ---------------------------------------------------------
    # 4. CROP
    # ---------------------------------------------------------

    crop = None

    if field:
        crop = db.query(Crop).filter(
            Crop.field_id == field.id
        ).first()

    # ---------------------------------------------------------
    # 5. LIVESTOCK
    # ---------------------------------------------------------

    livestock = []

    if farm:
        livestock_records = db.query(
            Livestock
        ).filter(
            Livestock.farm_id == farm.id
        ).all()

        livestock = [
            safe_dict(
                animal,
                [
                    "id",
                    "animal_tag",
                    "animal_type",
                    "breed",
                    "gender",
                    "weight",
                    "health_status",
                ],
            )
            for animal in livestock_records
        ]

    # ---------------------------------------------------------
    # 6. SENSORS
    # ---------------------------------------------------------

    sensors = []
    readings = []

    if field:

        sensor_records = db.query(
            Sensor
        ).filter(
            Sensor.field_id == field.id
        ).all()

        sensors = [
            safe_dict(
                sensor,
                [
                    "id",
                    "name",
                    "sensor_type",
                    "status",
                ],
            )
            for sensor in sensor_records
        ]

        for sensor in sensor_records:

            reading = db.query(
                SensorReading
            ).filter(
                SensorReading.sensor_id == sensor.id
            ).order_by(
                SensorReading.recorded_at.desc()
            ).first()

            if reading:

                readings.append({
                    "sensor_id": sensor.id,
                    "sensor_type": getattr(
                        sensor,
                        "sensor_type",
                        None,
                    ),
                    "value": getattr(
                        reading,
                        "value",
                        None,
                    ),
                    "unit": getattr(
                        reading,
                        "unit",
                        None,
                    ),
                    "recorded_at": getattr(
                        reading,
                        "recorded_at",
                        None,
                    ),
                })

    # ---------------------------------------------------------
    # 7. ALERTS
    # ---------------------------------------------------------

    alerts = []

    if field:

        alert_records = db.query(
            Alert
        ).filter(
            Alert.field_id == field.id
        ).order_by(
            Alert.created_at.desc()
        ).limit(20).all()

        alerts = [
            safe_dict(
                alert,
                [
                    "id",
                    "title",
                    "message",
                    "severity",
                    "status",
                    "created_at",
                ],
            )
            for alert in alert_records
        ]

    # ---------------------------------------------------------
    # 8. RECOMMENDATIONS
    # ---------------------------------------------------------

    recommendations = []

    if field:

        recommendation_records = db.query(
            Recommendation
        ).filter(
            Recommendation.field_id == field.id
        ).order_by(
            Recommendation.created_at.desc()
        ).limit(20).all()

        recommendations = [
            safe_dict(
                recommendation,
                [
                    "id",
                    "title",
                    "message",
                    "priority",
                    "status",
                    "created_at",
                ],
            )
            for recommendation in recommendation_records
        ]

    # ---------------------------------------------------------
    # 9. VERIFIED CONTEXT
    # ---------------------------------------------------------

    context = {
        "user": {
            "id": user.id,
            "name": user.name,
            "language": user.language,
        },

        "farm": safe_dict(
            farm,
            [
                "id",
                "name",
                "location",
            ],
        ),

        "field": safe_dict(
            field,
            [
                "id",
                "name",
                "survey_number",
                "area_acres",
                "latitude",
                "longitude",
                "village",
                "taluk",
                "district",
                "state",
            ],
        ),

        "crop": safe_dict(
            crop,
            [
                "id",
                "name",
                "variety",
                "stage",
            ],
        ),

        "livestock": livestock,

        "sensors": sensors,

        "iot": {
            "latest_readings": readings,
        },

        "alerts": alerts,

        "recommendations": recommendations,
    }

    # ---------------------------------------------------------
    # 10. SEND VERIFIED DATA TO AI SERVICE
    # ---------------------------------------------------------

    payload = {
        "user_id": str(user.id),
        "farm_id": str(farm.id) if farm else None,
        "field_id": str(field.id) if field else None,
        "language": request.language or user.language or "kn",
        "message": request.message,
        "context": context,
    }

    try:

        async with httpx.AsyncClient(
            timeout=120.0
        ) as client:

            response = await client.post(
                f"{AI_AGENT_URL}/api/v1/agent/chat",
                json=payload,
            )

            response.raise_for_status()

            return response.json()

    except httpx.HTTPError as exc:

        raise HTTPException(
            status_code=502,
            detail=f"AI service unavailable: {str(exc)}",
        )
    
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import text
from pydantic import BaseModel


TASK_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS kannadakrushi_ai_tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    farm_id INTEGER,
    field_id INTEGER,
    title VARCHAR(255) NOT NULL,
    details TEXT,
    scheduled_for TIMESTAMPTZ NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
"""


class TaskCreateRequest(BaseModel):
    title: str
    user_id: int
    details: str | None = None
    scheduled_for: datetime | None = None
    farm_id: int | None = None
    field_id: int | None = None
    language: str = "en"


def ensure_task_table(db: Session):
    db.execute(text(TASK_TABLE_SQL))


def task_dict(row):
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "farm_id": row["farm_id"],
        "field_id": row["field_id"],
        "title": row["title"],
        "details": row["details"],
        "scheduled_for": row["scheduled_for"].isoformat(),
        "status": row["status"],
        "language": row["language"],
        "created_at": row["created_at"].isoformat(),
        "updated_at": row["updated_at"].isoformat(),
    }


@router.post("/tasks")
def create_task(data: TaskCreateRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Task title is required")

    scheduled = data.scheduled_for or datetime.now(ZoneInfo("Asia/Kolkata"))
    if scheduled.tzinfo is None:
        scheduled = scheduled.replace(tzinfo=ZoneInfo("Asia/Kolkata"))

    try:
        ensure_task_table(db)
        result = db.execute(
            text("""
                INSERT INTO kannadakrushi_ai_tasks
                (user_id, farm_id, field_id, title, details, scheduled_for, language)
                VALUES
                (:user_id, :farm_id, :field_id, :title, :details, :scheduled_for, :language)
                RETURNING *
            """),
            {
                "user_id": data.user_id,
                "farm_id": data.farm_id,
                "field_id": data.field_id,
                "title": title,
                "details": data.details,
                "scheduled_for": scheduled,
                "language": data.language or "en",
            },
        )
        row = result.mappings().one()
        db.commit()
        return {"success": True, "task": task_dict(row)}
    except Exception:
        db.rollback()
        raise


def tasks_for_day(db: Session, user_id: int, offset: int):
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")

    target = datetime.now(ZoneInfo("Asia/Kolkata")).date() + timedelta(days=offset)

    try:
        ensure_task_table(db)
        result = db.execute(
            text("""
                SELECT * FROM kannadakrushi_ai_tasks
                WHERE user_id = :user_id
                  AND (scheduled_for AT TIME ZONE 'Asia/Kolkata')::date = :target
                ORDER BY scheduled_for
            """),
            {"user_id": user_id, "target": target},
        )
        rows = [task_dict(row) for row in result.mappings().all()]
        db.commit()
        return {
            "success": True,
            "date": target.isoformat(),
            "count": len(rows),
            "tasks": rows,
        }
    except Exception:
        db.rollback()
        raise


@router.get("/tasks/today")
def today_tasks(user_id: int, db: Session = Depends(get_db)):
    return tasks_for_day(db, user_id, 0)


@router.get("/tasks/tomorrow")
def tomorrow_tasks(user_id: int, db: Session = Depends(get_db)):
    return tasks_for_day(db, user_id, 1)


@router.post("/tasks/{task_id}/complete")
def complete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")

    try:
        ensure_task_table(db)
        result = db.execute(
            text("""
                UPDATE kannadakrushi_ai_tasks
                SET status = 'completed', updated_at = NOW()
                WHERE id = :task_id AND user_id = :user_id
                RETURNING *
            """),
            {"task_id": task_id, "user_id": user_id},
        )
        row = result.mappings().first()
        if row is None:
            db.rollback()
            raise HTTPException(status_code=404, detail="Task not found")
        db.commit()
        return {"success": True, "task": task_dict(row)}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise
