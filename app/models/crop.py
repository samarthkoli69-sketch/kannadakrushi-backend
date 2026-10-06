from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Crop(Base):
    __tablename__ = "crops"

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

    crop_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    variety: Mapped[str | None] = mapped_column(
        String(100)
    )

    season: Mapped[str | None] = mapped_column(
        String(50)
    )

    growth_stage: Mapped[str | None] = mapped_column(
        String(100)
    )

    sowing_date: Mapped[date | None] = mapped_column(
        Date
    )

    expected_harvest_date: Mapped[date | None] = mapped_column(
        Date
    )

    field = relationship(
        "Field",
        back_populates="crops"
    )