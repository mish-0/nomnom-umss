from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.schema import (
    UserCreate,
    UserLogin,
)

from app.modules.users.service import UserService


class UserController:

    @staticmethod
    async def register(
        db: AsyncSession,
        user: UserCreate,
    ):
        return await UserService.create_user(
            db,
            user,
        )

    @staticmethod
    async def login(
        db: AsyncSession,
        credentials: UserLogin,
    ):
        return await UserService.login(
            db,
            credentials,
        )