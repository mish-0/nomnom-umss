from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Review(Base):

    __tablename__ = "reviews"


    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "food_stall_id",
            name="uq_user_food_stall",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    rating: Mapped[int] = mapped_column(Integer)  

    comment: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    food_stall_id: Mapped[int] = mapped_column(
        ForeignKey("food_stalls.id", ondelete="CASCADE")
    )