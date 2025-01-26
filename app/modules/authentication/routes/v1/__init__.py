from fastapi import APIRouter

from .auth import auth_router

authentication_routers = APIRouter()

authentication_routers.include_router(
    auth_router, tags=["registration", "login"])
