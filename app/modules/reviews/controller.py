from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reviews.schema import ReviewCreate
from app.modules.reviews.service import ReviewService


class ReviewController:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: ReviewCreate,
        user_id: int,
    ):
        return await ReviewService.create(
            db,
            data,
            user_id,
        )

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):
        return await ReviewService.get_all(db)

    @staticmethod
    async def get_by_stall(
        db: AsyncSession,
        stall_id: int,
    ):
        return await ReviewService.get_by_stall(
            db,
            stall_id,
        )