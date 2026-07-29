from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import tasks


ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app = FastAPI(title="TaskForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "TaskForge backend is running!"}