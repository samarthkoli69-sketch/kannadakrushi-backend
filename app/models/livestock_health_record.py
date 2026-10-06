from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class LivestockHealthRecord(Base):
    __tablename__ = "livestock_health_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    livestock_id: Mapped[int] = mapped_column(
        ForeignKey("livestock.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    record_date: Mapped[date] = mapped_column(
        Date,
        default=lambda: datetime.now(timezone.utc).date(),
        nullable=False,
    )

    health_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    symptoms: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    treatment_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    veterinary_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    livestock = relationship(
        "Livestock",
        back_populates="health_records",
    )