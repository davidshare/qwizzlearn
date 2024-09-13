from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.dependencies import get_current_user, AccessTokenBearer
from src.db.main import get_session

from .controller import AuthorisationController
from .schemas import PermissionCreate, PermissionUpdate, RoleCreate, RoleUpdate, AssignPermissionToRole, AssignRoleToUser
from .dependencies import route_with_action, authorize

authorisation_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@route_with_action('create_permission')
@authorisation_router.post("/permissions", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED)
async def create_permission(permission_data: List[PermissionCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.create_permission(permission_data, user, session)


@route_with_action('get_all_permissions')
@authorisation_router.get("/permissions", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def get_all_permissions(session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_all_permissions(session)


@route_with_action('get_permission')
@authorisation_router.get("/permissions/{permission_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def get_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_permission_by_id(permission_id, session)


@route_with_action('get_permission_by_action')
@authorisation_router.get("/permissions/{permission_action}/action", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def get_permission_by_action(permission_action: str, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_permission_by_action(permission_action, session)


@route_with_action('update_permission')
@authorisation_router.put("/permissions/{permission_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def update_permission(permission_id: int, permission_data: PermissionUpdate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.update_permission(permission_id, permission_data, user, session)


@route_with_action('delete_permission')
@authorisation_router.delete("/permissions/{permission_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def delete_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.delete_permission(permission_id, session)


@route_with_action('create_role')
@authorisation_router.post("/roles", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_201_CREATED)
async def create_role(role_data: List[RoleCreate], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.create_role(role_data, user, session)


@route_with_action('update_role')
@ authorisation_router.put("/roles/{role_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def update_role(role_id: int, role_data: RoleUpdate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.update_role(role_id, role_data, user, session)


@ authorisation_router.get("/roles", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def get_all_roles(session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_all_roles(session)


@route_with_action('get_role')
@ authorisation_router.get("/roles/{role_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def get_role(role_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_role_by_id(role_id, session)


@route_with_action('get_role_by_name')
@ authorisation_router.get("/roles/{role_name}/name", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def get_role_by_name(role_name: str, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.get_role_by_name(role_name, session)


@route_with_action('delete_role')
@ authorisation_router.delete("/roles/{role_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def delete_role(role_id: int, session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.delete_role(role_id, session)


@route_with_action('assign_permission_to_role')
@ authorisation_router.post("/roles/permissions", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def assign_permission_to_role(permissions_data: List[AssignPermissionToRole], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.assign_permissions_to_role(permissions_data, user, session)


@route_with_action('assign_role_to_user')
@ authorisation_router.post("/roles/users", status_code=status.HTTP_200_OK)
async def assign_role_to_user(roles_data: List[AssignRoleToUser], user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.assign_roles_to_user(roles_data, user, session)


@route_with_action('revoke_user_roles')
@ authorisation_router.delete("/roles/users/{user_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def revoke_user_roles(user_id: int, role_ids: List[int], session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.revoke_user_roles(user_id, role_ids, session)


@route_with_action('revoke_role_permissions')
@ authorisation_router.delete("/roles/permissions/{role_id}", dependencies=[Depends(access_token_bearer), Depends(authorize)], status_code=status.HTTP_200_OK)
async def revoke_role_permissions(role_id: int, permission_ids: List[int], session: AsyncSession = Depends(get_session)):
    return await AuthorisationController.revoke_role_permissions(role_id, permission_ids, session)
