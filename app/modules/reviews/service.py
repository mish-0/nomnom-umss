from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.modules.reviews.model import Review
from app.modules.reviews.schema import ReviewCreate


class ReviewService:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: ReviewCreate,
        user_id: int,           
    ):
        existing = await db.execute(
            select(Review).where(
                Review.user_id == user_id,
                Review.food_stall_id == data.food_stall_id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail="Ya dejaste una reseña para este puesto.",
            )

        review = Review(
            rating=data.rating,
            comment=data.comment,
            user_id=user_id,
            food_stall_id=data.food_stall_id,
        )

        db.add(review)
        await db.commit()
        await db.refresh(review)

        return review

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Review))
        return result.scalars().all()

    @staticmethod
    async def get_by_stall(db: AsyncSession, stall_id: int):
        result = await db.execute(
            select(Review).where(Review.food_stall_id == stall_id)
        )
        return result.scalars().all()