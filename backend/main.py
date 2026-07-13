from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend import models
from backend.database import Base, engine
from backend.routers import tasks

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="TaskForge API",
    lifespan=lifespan,
)

app.include_router(tasks.router)

@app.get("/")
def home():
    return {"message": "TaskForge backend is running!"}