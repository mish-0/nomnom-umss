from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.modules.food_stalls.controller import (
    FoodStallController
)

from app.modules.food_stalls.schema import (
    FoodStallCreate,
    FoodStallResponse
)

router = APIRouter(
    prefix="/food-stalls",
    tags=["Food Stalls"]
)

DBSession = Annotated[
    AsyncSession,
    Depends(get_db)
]


@router.post(
    "/",
    response_model=FoodStallResponse
)
async def create_food_stall(
    data: FoodStallCreate,
    db: DBSession
):
    return await FoodStallController.create(
        db,
        data
    )


@router.get(
    "/",
    response_model=list[FoodStallResponse]
)
async def get_food_stalls(
    db: DBSession
):
    return await FoodStallController.get_all(
        db
    )