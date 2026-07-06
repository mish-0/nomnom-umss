from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role  

from app.modules.food_stalls.controller import FoodStallController
from app.modules.food_stalls.schema import FoodStallCreate, FoodStallResponse

router = APIRouter(prefix="/food-stalls", tags=["Food Stalls"])

DBSession = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "/",
    response_model=FoodStallResponse,
    status_code=201,
)
async def create_food_stall(
    data: FoodStallCreate,
    db: DBSession,
    current_user=Depends(require_role("DUENO")),  
):
    return await FoodStallController.create(
        db,
        data,
        owner_id=current_user.id,  
    )


@router.get(
    "/",
    response_model=list[FoodStallResponse],
)
async def get_food_stalls(db: DBSession):
    return await FoodStallController.get_all(db)