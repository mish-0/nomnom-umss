from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
import app.core.mapping_database

from app.modules.users.routes import router as auth_router
from app.modules.food_stalls.routes import router as food_stalls_router
from app.modules.menu.routes import router as menu_router
from app.modules.reviews.routes import router as reviews_router
from app.modules.ranking.routes import router as ranking_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="NomNom UMSS",
    description="""
## 🍜 NomNom UMSS API

Plataforma para comparar puestos de comida universitaria.

### Cómo autenticarse
1. Crea una cuenta con `POST /auth/register`
2. Obtén tu token con `POST /auth/login`
3. Haz clic en **Authorize 🔒** (arriba a la derecha)
4. Escribe `Bearer <tu_token>` en el campo y haz clic en Authorize
    """,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(food_stalls_router)
app.include_router(menu_router)
app.include_router(reviews_router)
app.include_router(ranking_router)



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in schema["paths"].values():
        for method in path.values():
            if "security" in method:
                method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


@app.get("/", tags=["Health"])
def home():
    return {"message": "NomNom UMSS API funcionando 🚀"}