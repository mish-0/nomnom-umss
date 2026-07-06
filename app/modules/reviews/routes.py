from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.modules.reviews.controller import ReviewController
from app.modules.reviews.schema import (
    ReviewCreate,
    ReviewResponse,
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)

DBSession = Annotated[
    AsyncSession,
    Depends(get_db),
]


@router.post(
    "/",
    response_model=ReviewResponse,
)
async def create_review(
    data: ReviewCreate,
    db: DBSession,
    current_user=Depends(get_current_user),
):
    return await ReviewController.create(
        db,
        data,
        user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[ReviewResponse],
)
async def get_reviews(
    db: DBSession,
):
    return await ReviewController.get_all(db)


@router.get(
    "/stall/{stall_id}",
    response_model=list[ReviewResponse],
)
async def get_reviews_by_stall(
    stall_id: int,
    db: DBSession,
):
    return await ReviewController.get_by_stall(
        db,
        stall_id,
    )