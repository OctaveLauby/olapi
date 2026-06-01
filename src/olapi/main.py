from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI

from olapi.settings import LOGGING_CONFIG
from olapi.db import Base, engine
from olapi.routers import auth, temporary

dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="olapi", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(temporary.router)
