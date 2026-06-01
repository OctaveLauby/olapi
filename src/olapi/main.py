from contextlib import asynccontextmanager

from fastapi import FastAPI

from olapi.db import Base, engine
from olapi.routers import auth, temporary


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="olapi", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(temporary.router)
