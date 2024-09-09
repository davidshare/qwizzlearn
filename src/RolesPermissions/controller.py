from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import RoleCreate, PermissionCreate, RoleUpdate, PermissionUpdate
from .service import RolePermissionService

role_permission_service = RolePermissionService()


class RolePermissionController:

    @staticmethod
    async def create_role(role_data: RoleCreate, session: AsyncSession):
        return await role_permission_service.create_role(role_data, session)

    @staticmethod
    async def create_permission(permission_data: PermissionCreate, session: AsyncSession):
        return await role_permission_service.create_permission(permission_data, session)

    @staticmethod
    async def assign_permission_to_role(role_id: int, permission_id: int, session: AsyncSession):
        role = await role_permission_service.assign_permission_to_role(role_id, permission_id, session)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role or Permission not found")
        return role

    @staticmethod
    async def get_role(role_id: int, session: AsyncSession):
        role = await role_permission_service.get_role(role_id, session)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return role

    @staticmethod
    async def get_permission(permission_id: int, session: AsyncSession):
        permission = await role_permission_service.get_permission(permission_id, session)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return permission

    @staticmethod
    async def get_all_roles(session: AsyncSession):
        return await role_permission_service.get_all_roles(session)

    @staticmethod
    async def get_all_permissions(session: AsyncSession):
        return await role_permission_service.get_all_permissions(session)

    @staticmethod
    async def update_role(role_id: int, role_data: RoleUpdate, session: AsyncSession):
        role = await role_permission_service.get_role(role_id, session)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return await role_permission_service.update_role(role_id, role_data, session)

    @staticmethod
    async def delete_role(role_id: int, session: AsyncSession):
        role = await role_permission_service.get_role(role_id, session)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return await role_permission_service.delete_role(role_id, session)

    @staticmethod
    async def update_permission(permission_id: int, permission_data: PermissionUpdate, session: AsyncSession):
        permission = await role_permission_service.get_permission(permission_id, session)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return await role_permission_service.update_permission(permission_id, permission_data, session)

    @staticmethod
    async def delete_permission(permission_id: int, session: AsyncSession):
        permission = await role_permission_service.get_permission(permission_id, session)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return await role_permission_service.delete_permission(permission_id, session)
