from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from database import engine
from settings import settings


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield
    await engine.dispose()


def get_app() -> FastAPI:
    fast_api = FastAPI(lifespan=app_lifespan)
    fast_api.include_router(api_router)
    return fast_api


app = get_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
