from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Review(Base):

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    rating: Mapped[int] = mapped_column(
        Integer
    )

    comment: Mapped[str] = mapped_column(
        String(500)
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    food_stall_id: Mapped[int] = mapped_column(
        ForeignKey("food_stalls.id")
    )