from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.menu.model import MenuItem
from app.modules.menu.schema import MenuItemCreate


class MenuService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: MenuItemCreate,
    ):

        item = MenuItem(
            name=data.name,
            price=data.price,
            available=data.available,
            food_stall_id=data.food_stall_id,
        )

        db.add(item)

        await db.commit()

        await db.refresh(item)

        return item

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):

        result = await db.execute(
            select(MenuItem)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_stall(
        db: AsyncSession,
        stall_id: int,
    ):

        result = await db.execute(
            select(MenuItem).where(
                MenuItem.food_stall_id == stall_id
            )
        )

        return result.scalars().all()