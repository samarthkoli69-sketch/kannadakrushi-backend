from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Livestock(Base):
    __tablename__ = "livestock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    animal_tag: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    animal_type: Mapped[str] = mapped_column(String(50), nullable=False)
    breed: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)

    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)

    health_status: Mapped[str] = mapped_column(
        String(50),
        default="healthy",
        nullable=False,
    )

    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    farm = relationship("Farm", back_populates="livestock")

    health_records = relationship(
        "LivestockHealthRecord",
        back_populates="livestock",
        cascade="all, delete-orphan",
    )

    vaccinations = relationship(
        "LivestockVaccination",
        back_populates="livestock",
        cascade="all, delete-orphan",
    )