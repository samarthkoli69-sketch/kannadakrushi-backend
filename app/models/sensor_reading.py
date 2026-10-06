from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    field_id: Mapped[int] = mapped_column(
        ForeignKey("fields.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    soil_moisture: Mapped[float | None] = mapped_column(Float)

    soil_temperature: Mapped[float | None] = mapped_column(Float)

    soil_ph: Mapped[float | None] = mapped_column(Float)

    air_temperature: Mapped[float | None] = mapped_column(Float)

    humidity: Mapped[float | None] = mapped_column(Float)

    water_level: Mapped[float | None] = mapped_column(Float)

    rainfall: Mapped[float | None] = mapped_column(Float)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    sensor = relationship(
        "Sensor",
        back_populates="readings"
    )

    field = relationship(
        "Field",
        back_populates="sensor_readings"
    )