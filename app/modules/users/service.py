from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.modules.users.model import User
from app.modules.users.schema import UserCreate, UserLogin


class UserService:

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ):
        query = select(User).where(User.email == email)

        result = await db.execute(query)

        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        user: UserCreate,
    ):

        existing = await UserService.get_by_email(
            db,
            user.email,
        )

        if existing:
            raise Exception("El correo ya está registrado")

        new_user = User(
            name=user.name,
            last_name=user.last_name,
            email=user.email,
            password=hash_password(user.password),
            role=user.role,
        )

        db.add(new_user)

        await db.commit()

        await db.refresh(new_user)

        return new_user

    @staticmethod
    async def login(
        db: AsyncSession,
        credentials: UserLogin,
    ):

        user = await UserService.get_by_email(
            db,
            credentials.email,
        )

        if not user:
            raise Exception("Usuario no encontrado")

        if not verify_password(
            credentials.password,
            user.password,
        ):
            raise Exception("Contraseña incorrecta")

        token = create_access_token(
            {
                "sub": user.email
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }