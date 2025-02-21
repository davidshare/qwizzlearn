from typing import Callable
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import config
from app.core.database import db_init
from app.core.exceptions import (
    DuplicateEntryException,
    InternalServerException,
    ValidationException,
)
from app.core.logger import CustomLogger
from app.core.middleware import (
    duplicate_entry_handler,
    internal_server_error_handler,
    validation_exception_handler,
)

from app.modules.authentication.routes.v1 import authentication_routers

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting...")
    await db_init()
    yield
    print("server has been stopped...")


app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
)

origins = [
    config.FRONTEND_ORIGIN,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Set-Cookie",
    ],
    expose_headers=["Set-Cookie"],
)

app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(DuplicateEntryException, duplicate_entry_handler)
app.add_exception_handler(InternalServerException, internal_server_error_handler)

logger = CustomLogger()


@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    logger.log_request(request)
    try:
        response = await call_next(request)
        logger.log_response(response)
        return response
    except Exception as exc:
        logger.log_exception(exc)
        raise


@app.get("/")
def read_root():
    return {"message": "Welcome to qwizzlearn api!!!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(
    authentication_routers, prefix="/api/v1/auth", tags=["authentication"]
)
