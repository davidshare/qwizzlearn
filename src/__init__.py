from contextlib import asynccontextmanager

from fastapi import FastAPI


from src.db.main import db_init

from src.authentication.router import authentication_router
from src.authorisation.router import authorisation_router
from src.difficulty.router import difficulty_router
from src.categories.router import category_router


@asynccontextmanager
async def life_span(lifespan_app: FastAPI):
    print("server is starting...")
    await db_init()
    yield
    print("Server has been stopped. ..")


VERSION = "v1"

app = FastAPI(
    title="Qwizzlearn",
    description="An application that lets people take quizzes and compete",
    version=VERSION,
    lifespan=life_span
)


@app.get('/')
async def read_root():
    return {
        "message": "Hello world!"
    }

app.include_router(
    authentication_router, prefix='/api/{VERSION}/auth', tags=['authentication'])
app.include_router(
    authorisation_router, prefix='/api/{VERSION}/authorisation', tags=['authorisation'])
app.include_router(
    difficulty_router, prefix='/api/{VERSION}/difficulties', tags=['difficulty'])
app.include_router(
    category_router, prefix='/api/{VERSION}/categories', tags=['category'])
