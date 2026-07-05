from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.food_stalls.schema import FoodStallCreate
from app.modules.food_stalls.service import FoodStallService


class FoodStallController:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: FoodStallCreate
    ):
        return await FoodStallService.create(
            db,
            data
        )

    @staticmethod
    async def get_all(
        db: AsyncSession
    ):
        return await FoodStallService.get_all(db)