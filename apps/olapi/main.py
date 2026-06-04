from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import APIRouter, Depends, FastAPI

from auth import check_authentication
from database import engine
from models.base import BaseModel
from routers import auth, temporary
from settings import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    BaseModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="olapi", lifespan=lifespan)
app_router = APIRouter(dependencies=[Depends(check_authentication)])
app.include_router(auth.router)
app.include_router(temporary.router)
