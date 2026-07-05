from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ranking.service import RankingService


class RankingController:

    @staticmethod
    async def get_ranking(
        db: AsyncSession,
    ):
        return await RankingService.get_ranking(db)