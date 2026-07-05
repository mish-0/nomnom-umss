from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reviews.model import Review
from app.modules.reviews.schema import ReviewCreate


class ReviewService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: ReviewCreate,
    ):

        review = Review(
            rating=data.rating,
            comment=data.comment,
            user_id=data.user_id,
            food_stall_id=data.food_stall_id,
        )

        db.add(review)

        await db.commit()

        await db.refresh(review)

        return review

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):

        result = await db.execute(
            select(Review)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_stall(
        db: AsyncSession,
        stall_id: int,
    ):

        result = await db.execute(
            select(Review).where(
                Review.food_stall_id == stall_id
            )
        )

        return result.scalars().all()