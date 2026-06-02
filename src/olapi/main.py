from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import APIRouter, Depends, FastAPI

from olapi.auth import check_authentication
from olapi.database import engine
from olapi.models.base import BaseModel
from olapi.routers import auth, temporary
from olapi.settings import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    BaseModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="olapi", lifespan=lifespan)
app_router = APIRouter(dependencies=[Depends(check_authentication)])
app.include_router(auth.router)
app.include_router(temporary.router)
