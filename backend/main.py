from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os

from backend.routers import auth, tasks


LOCAL_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def get_allowed_origins() -> list[str]:
    origins = LOCAL_ORIGINS.copy()

    frontend_origin = os.getenv("FRONTEND_ORIGIN")

    if frontend_origin:
        frontend_origin = frontend_origin.strip().rstrip("/")

        if frontend_origin:
            origins.append(frontend_origin)

    return origins


ALLOWED_ORIGINS = get_allowed_origins()


app = FastAPI(title="TaskForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "TaskForge backend is running!"}