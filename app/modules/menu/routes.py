from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role

from app.modules.menu.controller import MenuController
from app.modules.menu.schema import (
    MenuItemCreate,
    MenuItemResponse,
)

router = APIRouter(
    prefix="/menu",
    tags=["Menu"],
)

DBSession = Annotated[
    AsyncSession,
    Depends(get_db),
]


@router.post(
    "/",
    response_model=MenuItemResponse,
)
async def create_menu_item(
    data: MenuItemCreate,
    db: DBSession,
    current_user=Depends(require_role("DUENO")),
):
    return await MenuController.create(
        db,
        data,
    )


@router.get(
    "/",
    response_model=list[MenuItemResponse],
)
async def get_menu(
    db: DBSession,
):
    return await MenuController.get_all(db)


@router.get(
    "/stall/{stall_id}",
    response_model=list[MenuItemResponse],
)
async def get_menu_by_stall(
    stall_id: int,
    db: DBSession,
):
    return await MenuController.get_by_stall(
        db,
        stall_id,
    )