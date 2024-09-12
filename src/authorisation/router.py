from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.dependencies import get_current_user, AccessTokenBearer
from src.db.main import get_session

from .controller import AuthorisationController
from .schemas import PermissionCreate, PermissionUpdate, RoleCreate, RoleUpdate

authorisation_router = APIRouter()


@authorisation_router.post("/permissions", status_code=status.HTTP_201_CREATED)
async def create_permission(permission_data: List[PermissionCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.create_permission(permission_data, user, session)


@authorisation_router.get("/permissions", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def get_all_permissions(session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_all_permissions(session)


@authorisation_router.get("/permissions/{permission_id}", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def get_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_permission_by_id(permission_id, session)


@authorisation_router.get("/permissions/{permission_action}/action", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def get_permission_by_action(permission_action: str, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_permission_by_action(permission_action, session)


@authorisation_router.put("/permissions/{permission_id}", status_code=status.HTTP_200_OK)
async def update_permission(permission_id: int, permission_data: PermissionUpdate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.update_permission(permission_id, permission_data, user, session)


@authorisation_router.delete("/permissions/{permission_id}", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def delete_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.delete_permission(permission_id, session)


@authorisation_router.post("/roles", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_201_CREATED)
async def create_role(role_data: List[RoleCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.create_role(role_data, user, session)


@ authorisation_router.put("/roles/{role_id}", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def update_role(role_id: int, role_data: RoleUpdate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.update_role(role_id, role_data, user, session)


@ authorisation_router.get("/roles", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def get_all_roles(session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_all_roles(session)


@ authorisation_router.get("/roles/{role_id}", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def get_role(role_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_role_by_id(role_id, session)


@ authorisation_router.get("/roles/{role_name}/name", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def get_role_by_name(role_name: str, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_role_by_name(role_name, session)


@ authorisation_router.post("/roles/{role_id}/permissions/{permission_id}", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def assign_permission_to_role(role_id: int, permission_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.assign_permission_to_role(role_id, permission_id, session)


@ authorisation_router.delete("/roles/{role_id}", dependencies=[Depends(AccessTokenBearer())], status_code=status.HTTP_200_OK)
async def delete_role(role_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.delete_role(role_id, session)
