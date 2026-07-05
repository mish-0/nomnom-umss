from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.menu.schema import MenuItemCreate
from app.modules.menu.service import MenuService


class MenuController:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: MenuItemCreate,
    ):
        return await MenuService.create(
            db,
            data,
        )

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):
        return await MenuService.get_all(db)

    @staticmethod
    async def get_by_stall(
        db: AsyncSession,
        stall_id: int,
    ):
        return await MenuService.get_by_stall(
            db,
            stall_id,
        )
