from fastapi import FastAPI
from contextlib import asynccontextmanager
from tortoise import Tortoise
from core.config import settings
from routers import auth_router, permission_router, task_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": settings.MODELS}
    )
    yield
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router.router, tags=["auth"])
app.include_router(task_router.router, tags=["tasks"])
app.include_router(permission_router.router, tags=["permission"])



