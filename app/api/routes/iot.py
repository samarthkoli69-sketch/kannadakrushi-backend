
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.farm import Farm
from app.models.field import Field
from app.models.sensor import Sensor
from app.models.sensor_reading import SensorReading
from app.models.user import User
from app.schemas.iot import (
    DeviceRegistrationCreate,
    IoTReadingCreate,
    SensorResponse,
)


router = APIRouter()


# ============================================================
# REGISTER DEVICE
# POST /api/v1/iot/devices
# ============================================================

@router.post(
    "/devices",
    response_model=SensorResponse,
    status_code=201,
)
def register_device(
    data: DeviceRegistrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device_id = data.device_id.strip()

    if not device_id:
        raise HTTPException(
            status_code=422,
            detail="Device ID is required",
        )

    if len(device_id) > 100:
        raise HTTPException(
            status_code=422,
            detail="Device ID cannot exceed 100 characters",
        )

    # Verify that this field belongs to the signed-in farmer.
    field = (
        db.query(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .filter(
            Field.id == data.field_id,
            Farm.owner_id == current_user.id,
        )
        .first()
    )

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found",
        )

    # Prevent duplicate device IDs and accidental reassignment.
    existing_sensor = (
        db.query(Sensor)
        .filter(Sensor.device_id == device_id)
        .first()
    )

    if existing_sensor:
        if existing_sensor.field_id != data.field_id:
            raise HTTPException(
                status_code=409,
                detail="This device is already assigned to another field",
            )

        # Return the existing device if it is already assigned here.
        return existing_sensor

    device_type = (data.device_type or "").strip() or "ESP32"

    if len(device_type) > 100:
        raise HTTPException(
            status_code=422,
            detail="Device type cannot exceed 100 characters",
        )

    device_name = data.name.strip() if data.name else None

    if device_name == "":
        device_name = None

    if device_name and len(device_name) > 100:
        raise HTTPException(
            status_code=422,
            detail="Device name cannot exceed 100 characters",
        )

    sensor = Sensor(
        device_id=device_id,
        field_id=data.field_id,
        device_type=device_type,
        name=device_name,
        is_active=True,
    )

    db.add(sensor)

    try:
        db.commit()
        db.refresh(sensor)
    except Exception:
        db.rollback()
        raise

    return sensor


# ============================================================
# LIST DEVICES REGISTERED TO A FIELD
# GET /api/v1/iot/fields/{field_id}/devices
# ============================================================

@router.get(
    "/fields/{field_id}/devices",
    response_model=list[SensorResponse],
)
def list_field_devices(
    field_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify the field belongs to the signed-in farmer.
    field = (
        db.query(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .filter(
            Field.id == field_id,
            Farm.owner_id == current_user.id,
        )
        .first()
    )

    if field is None:
        raise HTTPException(
            status_code=404,
            detail="Field not found",
        )

    return (
        db.query(Sensor)
        .filter(Sensor.field_id == field_id)
        .order_by(Sensor.id.asc())
        .all()
    )


# ============================================================
# RECEIVE IOT READING
# POST /api/v1/iot/readings
# ============================================================

@router.post("/readings")
def receive_reading(
    data: IoTReadingCreate,
    db: Session = Depends(get_db),
):
    sensor = (
        db.query(Sensor)
        .filter(Sensor.device_id == data.device_id)
        .first()
    )

    if not sensor:
        # Preserve the existing automatic-registration behavior
        # for devices that submit their first reading.
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
        # Do not accept readings for a field other than the one
        # to which this registered device is assigned.
        if sensor.field_id != data.field_id:
            raise HTTPException(
                status_code=409,
                detail="Device is registered to a different field",
            )

        sensor.last_seen = datetime.now(timezone.utc)

    reading = SensorReading(
        sensor_id=sensor.id,
        field_id=sensor.field_id,
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
        "device_id": sensor.device_id,
        "field_id": sensor.field_id,
    }


# ============================================================
# GET LATEST READING FOR A FIELD
# GET /api/v1/iot/fields/{field_id}/latest
# ============================================================

@router.get("/fields/{field_id}/latest")
def latest_reading(
    field_id: int,
    db: Session = Depends(get_db),
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
            detail="No sensor reading found",
        )

    return reading


# ============================================================
# GET READING HISTORY FOR A FIELD
# GET /api/v1/iot/fields/{field_id}/history
# ============================================================

@router.get("/fields/{field_id}/history")
def reading_history(
    field_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 200))

    return (
        db.query(SensorReading)
        .filter(SensorReading.field_id == field_id)
        .order_by(SensorReading.recorded_at.desc())
        .limit(limit)
        .all()
    )
