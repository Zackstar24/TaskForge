from fastapi import FastAPI

from backend.routers import tasks


app = FastAPI(title="TaskForge API")

app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "TaskForge backend is running!"}