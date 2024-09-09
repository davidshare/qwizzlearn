from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from .controller import RolePermissionController
from .schemas import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate

role_permission_router = APIRouter()


@role_permission_router.post("/roles", status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreate, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.create_role(role_data, session)


@role_permission_router.post("/permissions", status_code=status.HTTP_201_CREATED)
async def create_permission(permission_data: PermissionCreate, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.create_permission(permission_data, session)


@role_permission_router.post("/roles/{role_id}/permissions/{permission_id}", status_code=status.HTTP_200_OK)
async def assign_permission_to_role(role_id: int, permission_id: int, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.assign_permission_to_role(role_id, permission_id, session)


@role_permission_router.get("/roles", status_code=status.HTTP_200_OK)
async def get_all_roles(session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.get_all_roles(session)


@role_permission_router.get("/permissions", status_code=status.HTTP_200_OK)
async def get_all_permissions(session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.get_all_permissions(session)


@role_permission_router.get("/roles/{role_id}", status_code=status.HTTP_200_OK)
async def get_role(role_id: int, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.get_role(role_id, session)


@role_permission_router.get("/permissions/{permission_id}", status_code=status.HTTP_200_OK)
async def get_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.get_permission(permission_id, session)


@role_permission_router.put("/roles/{role_id}", status_code=status.HTTP_200_OK)
async def update_role(role_id: int, role_data: RoleUpdate, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.update_role(role_id, role_data, session)

# Delete role


@role_permission_router.delete("/roles/{role_id}", status_code=status.HTTP_200_OK)
async def delete_role(role_id: int, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.delete_role(role_id, session)

# Update permission


@role_permission_router.put("/permissions/{permission_id}", status_code=status.HTTP_200_OK)
async def update_permission(permission_id: int, permission_data: PermissionUpdate, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.update_permission(permission_id, permission_data, session)

# Delete permission


@role_permission_router.delete("/permissions/{permission_id}", status_code=status.HTTP_200_OK)
async def delete_permission(permission_id: int, session: AsyncSession = Depends(get_session)):
    return await RolePermissionController.delete_permission(permission_id, session)
