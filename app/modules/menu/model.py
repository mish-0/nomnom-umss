from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MenuItem(Base):

    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    price: Mapped[float] = mapped_column(
        Float
    )

    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    food_stall_id: Mapped[int] = mapped_column(
        ForeignKey("food_stalls.id")
    )