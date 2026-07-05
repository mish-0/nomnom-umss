from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.modules.ranking.controller import RankingController

router = APIRouter(
    prefix="/ranking",
    tags=["Ranking"],
)

DBSession = Annotated[
    AsyncSession,
    Depends(get_db),
]


@router.get("/")
async def get_ranking(
    db: DBSession,
):
    return await RankingController.get_ranking(
        db
    )