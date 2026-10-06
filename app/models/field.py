from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    survey_number: Mapped[str | None] = mapped_column(
        String(100),
        index=True
    )

    area_acres: Mapped[float | None] = mapped_column(
        Float
    )

    latitude: Mapped[float | None] = mapped_column(
        Float
    )

    longitude: Mapped[float | None] = mapped_column(
        Float
    )

    village: Mapped[str | None] = mapped_column(
        String(100)
    )

    taluk: Mapped[str | None] = mapped_column(
        String(100)
    )

    district: Mapped[str | None] = mapped_column(
        String(100)
    )

    state: Mapped[str] = mapped_column(
        String(100),
        default="Karnataka"
    )

    boundary_geojson: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    satellite_monitoring_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    last_satellite_check: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    latest_ndvi: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    latest_satellite_status: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    farm = relationship(
        "Farm",
        back_populates="fields"
    )

    crops = relationship(
        "Crop",
        back_populates="field",
        cascade="all, delete-orphan"
    )

    sensors = relationship(
        "Sensor",
        back_populates="field",
        cascade="all, delete-orphan"
    )

    sensor_readings = relationship(
        "SensorReading",
        back_populates="field",
        cascade="all, delete-orphan"
    )

    disease_scans = relationship(
        "DiseaseScan",
        back_populates="field",
        cascade="all, delete-orphan"
    )

    alerts = relationship(
        "Alert",
        back_populates="field",
        cascade="all, delete-orphan"
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="field",
        cascade="all, delete-orphan"
    )