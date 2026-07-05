from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.food_stalls.model import FoodStall
from app.modules.food_stalls.schema import FoodStallCreate


class FoodStallService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: FoodStallCreate
    ):

        stall = FoodStall(
            name=data.name,
            description=data.description,
            location=data.location,
            schedule=data.schedule,
            phone=data.phone,
            owner_id=data.owner_id
        )

        db.add(stall)

        await db.commit()

        await db.refresh(stall)

        return stall

    @staticmethod
    async def get_all(
        db: AsyncSession
    ):

        query = select(FoodStall)

        result = await db.execute(query)

        return result.scalars().all()