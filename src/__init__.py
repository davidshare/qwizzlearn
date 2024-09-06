from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import db_init


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is starting...")
    await db_init()
    yield
    print("Server has been stopped. ..")


version = "v1"

app = FastAPI(
    title="Qwizzlearn",
    description="An application that lets people take quizzes and compete",
    version=version,
    lifespan=life_span
)


@app.get('/')
async def read_root():
    return {
        "message": "Hello world!"
    }
