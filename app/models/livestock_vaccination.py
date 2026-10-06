from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class LivestockVaccination(Base):
    __tablename__ = "livestock_vaccinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    livestock_id: Mapped[int] = mapped_column(
        ForeignKey("livestock.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    vaccine_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    vaccination_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    next_due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
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
        back_populates="vaccinations",
    )