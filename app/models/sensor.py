from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    device_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    field_id: Mapped[int] = mapped_column(
        ForeignKey("fields.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    device_type: Mapped[str] = mapped_column(
        String(100),
        default="ESP32"
    )

    name: Mapped[str | None] = mapped_column(
        String(100)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    field = relationship(
        "Field",
        back_populates="sensors"
    )

    readings = relationship(
        "SensorReading",
        back_populates="sensor",
        cascade="all, delete-orphan"
    )