from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

DBSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DBSession,
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    from app.modules.users.service import UserService

    user = await UserService.get_by_email(db, payload["sub"])

    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user


# ── NUEVO ──────────────────────────────────────────────────────
# Dependencia que exige un rol específico.
# Uso en una ruta: current_user: Annotated[User, Depends(require_role("DUENO"))]
def require_role(*roles: str):
    async def _check(
        current_user=Depends(get_current_user),
    ):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado. Se requiere rol: {list(roles)}",
            )
        return current_user

    return _check