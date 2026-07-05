from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Base, engine
import app.core.mapping_database

from app.modules.users.routes import router as auth_router
from app.modules.food_stalls.routes import router as food_stalls_router

from app.modules.menu.routes import router as menu_router
from app.modules.reviews.routes import router as reviews_router
from app.modules.ranking.routes import router as ranking_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="NomNom UMSS",
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

@app.get("/")
def home():
    return {
        "message": "NomNom UMSS API funcionando 🚀"
    }