from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.users.controller import UserController
from app.modules.users.schema import (
    UserCreate,
    UserLogin,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

DBSession = Annotated[
    AsyncSession,
    Depends(get_db)
]


@router.post(
    "/register",
    response_model=UserResponse
)
async def register(
    user: UserCreate,
    db: DBSession,
):
    try:
        return await UserController.register(
            db,
            user,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login")
async def login(
    credentials: UserLogin,
    db: DBSession,
):
    try:
        return await UserController.login(
            db,
            credentials,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )