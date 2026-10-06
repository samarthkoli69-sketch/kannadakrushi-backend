from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.sensor import Sensor
from app.models.sensor_reading import SensorReading
from app.schemas.iot import IoTReadingCreate


router = APIRouter()


@router.post("/readings")
def receive_reading(
    data: IoTReadingCreate,
    db: Session = Depends(get_db)
):
    sensor = db.query(Sensor).filter(
        Sensor.device_id == data.device_id
    ).first()

    if not sensor:
        sensor = Sensor(
            device_id=data.device_id,
            field_id=data.field_id,
            device_type="ESP32",
            is_active=True,
            last_seen=datetime.now(timezone.utc),
        )

        db.add(sensor)
        db.flush()

    else:
        sensor.last_seen = datetime.now(timezone.utc)

    reading = SensorReading(
        sensor_id=sensor.id,
        field_id=data.field_id,
        soil_moisture=data.soil_moisture,
        soil_temperature=data.soil_temperature,
        soil_ph=data.soil_ph,
        air_temperature=data.air_temperature,
        humidity=data.humidity,
        water_level=data.water_level,
        rainfall=data.rainfall,
        recorded_at=data.recorded_at or datetime.now(timezone.utc),
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    return {
        "success": True,
        "message": "IoT reading stored",
        "reading_id": reading.id,
        "device_id": data.device_id,
        "field_id": data.field_id,
    }


@router.get("/fields/{field_id}/latest")
def latest_reading(
    field_id: int,
    db: Session = Depends(get_db)
):
    reading = (
        db.query(SensorReading)
        .filter(SensorReading.field_id == field_id)
        .order_by(SensorReading.recorded_at.desc())
        .first()
    )

    if not reading:
        raise HTTPException(
            status_code=404,
            detail="No sensor reading found"
        )

    return reading


@router.get("/fields/{field_id}/history")
def reading_history(
    field_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return (
        db.query(SensorReading)
        .filter(SensorReading.field_id == field_id)
        .order_by(SensorReading.recorded_at.desc())
        .limit(limit)
        .all()
    )