from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.food_stalls.model import FoodStall
from app.modules.reviews.model import Review

# Parámetro de confianza del Bayesian Average (ver README).
CONFIDENCE = 10


class RankingService:

    @staticmethod
    async def get_ranking(
        db: AsyncSession,
    ):
        # Promedio global (m) de TODAS las reseñas del sistema.
        global_avg_result = await db.execute(
            select(func.avg(Review.rating))
        )
        global_avg = global_avg_result.scalar()
        m = float(global_avg) if global_avg is not None else 0.0

        # LEFT JOIN para que los puestos sin reseñas también aparezcan
        # (con total_reviews = 0), en vez de desaparecer del ranking.
        query = (
            select(
                FoodStall.id,
                FoodStall.name,
                FoodStall.location,
                func.coalesce(func.avg(Review.rating), 0).label(
                    "average_rating"
                ),
                func.coalesce(func.sum(Review.rating), 0).label(
                    "rating_sum"
                ),
                func.count(Review.id).label("total_reviews"),
            )
            .outerjoin(
                Review,
                FoodStall.id == Review.food_stall_id,
            )
            .group_by(
                FoodStall.id,
                FoodStall.name,
                FoodStall.location,
            )
        )

        result = await db.execute(query)

        ranking = []

        for row in result.all():
            n = row.total_reviews
            rating_sum = float(row.rating_sum)

            # bayesian_score = (C * m + Σ ratings) / (C + n)
            bayesian_score = (CONFIDENCE * m + rating_sum) / (
                CONFIDENCE + n
            )

            ranking.append(
                {
                    "id": row.id,
                    "name": row.name,
                    "location": row.location,
                    "average_rating": round(
                        float(row.average_rating), 2
                    ),
                    "bayesian_score": round(bayesian_score, 2),
                    "total_reviews": n,
                }
            )

        ranking.sort(key=lambda r: r["bayesian_score"], reverse=True)

        return ranking