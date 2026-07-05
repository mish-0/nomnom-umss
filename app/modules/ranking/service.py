from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.food_stalls.model import FoodStall
from app.modules.reviews.model import Review


class RankingService:

    @staticmethod
    async def get_ranking(
        db: AsyncSession,
    ):

        query = (
            select(
                FoodStall.id,
                FoodStall.name,
                func.avg(Review.rating).label("average_rating"),
                func.count(Review.id).label("total_reviews"),
            )
            .join(
                Review,
                FoodStall.id == Review.food_stall_id,
            )
            .group_by(
                FoodStall.id,
                FoodStall.name,
            )
            .order_by(
                func.avg(Review.rating).desc()
            )
        )

        result = await db.execute(query)

        ranking = []

        for row in result.all():

            ranking.append(
                {
                    "id": row.id,
                    "name": row.name,
                    "average_rating": round(
                        float(row.average_rating), 2
                    ),
                    "total_reviews": row.total_reviews,
                }
            )

        return ranking