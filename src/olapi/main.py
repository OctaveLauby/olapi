from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI

from olapi.database import engine
from olapi.models.base import BaseModel
from olapi.routers import auth, temporary
from olapi.settings import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    BaseModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="olapi", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(temporary.router)
