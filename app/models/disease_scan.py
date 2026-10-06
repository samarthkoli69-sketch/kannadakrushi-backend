from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class DiseaseScan(Base):
    __tablename__ = "disease_scans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    field_id: Mapped[int] = mapped_column(
        ForeignKey("fields.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    image_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    predicted_issue: Mapped[str | None] = mapped_column(
        String(200)
    )

    confidence: Mapped[float | None] = mapped_column(
        Float
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    notes: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    field = relationship(
        "Field",
        back_populates="disease_scans"
    )