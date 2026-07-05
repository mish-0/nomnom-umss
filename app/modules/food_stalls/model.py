from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class FoodStall(Base):

    __tablename__ = "food_stalls"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    description: Mapped[str] = mapped_column(
        String(500)
    )

    location: Mapped[str] = mapped_column(
        String(200)
    )

    schedule: Mapped[str] = mapped_column(
        String(100)
    )

    phone: Mapped[str] = mapped_column(
        String(20)
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )