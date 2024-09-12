from typing import List
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.models import User
from .schemas import RoleCreate, PermissionCreate, RoleUpdate, PermissionUpdate
from .service import AuthorisationService
from .exceptions import PermissionNotFoundException, RoleNotFoundException

authorisation_service = AuthorisationService()


class AuthorisationController:

    @staticmethod
    async def create_permission(permission_data: List[PermissionCreate], user: User, session: AsyncSession):
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create permissions."
            )

        return await authorisation_service.create_permission(permission_data, user.id, session)

    @staticmethod
    async def update_permission(permission_id: int, permission_data: PermissionUpdate, user: User, session: AsyncSession):
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create permissions."
            )

        try:
            permission = await authorisation_service.update_permission(permission_id, permission_data, user, session)
            return permission
        except PermissionNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
            ) from exc

    @staticmethod
    async def get_all_permissions(session: AsyncSession):
        return await authorisation_service.get_all_permissions(session)

    @staticmethod
    async def get_permission_by_id(permission_id: int, session: AsyncSession):
        permission = await authorisation_service.get_permission_by_id(permission_id, session)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return permission

    @staticmethod
    async def get_permission_by_action(permission_action: str, session: AsyncSession):
        permission = await authorisation_service.get_permission_by_action(permission_action, session)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
        return permission

    @staticmethod
    async def delete_permission(permission_id: int, session: AsyncSession):
        try:
            return await authorisation_service.delete_permission(permission_id, session)
        except PermissionNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
            ) from exc

    @staticmethod
    async def create_role(role_data: List[RoleCreate], user: User, session: AsyncSession):

        try:
            role = await authorisation_service.create_role(role_data, user, session)
            return role
        except RoleNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            ) from exc

    @staticmethod
    async def update_role(role_id: int, role_data: RoleUpdate, user: User, session: AsyncSession):
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create permissions."
            )
        try:
            return await authorisation_service.update_role(role_id, role_data, user, session)
        except RoleNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            ) from exc

    @staticmethod
    async def get_all_roles(session: AsyncSession):
        return await authorisation_service.get_all_roles(session)

    @staticmethod
    async def get_role_by_id(role_id: int, session: AsyncSession):
        try:
            role = await authorisation_service.get_role_by_id(role_id, session)
            return role
        except RoleNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            ) from exc

    @staticmethod
    async def get_role_by_name(role_name: str, session: AsyncSession):
        try:
            role = await authorisation_service.get_role_by_name(role_name, session)
            return role
        except RoleNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
            ) from exc

    @staticmethod
    async def assign_permission_to_role(role_id: int, permission_id: int, session: AsyncSession):
        role = await authorisation_service.assign_permission_to_role(role_id, permission_id, session)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role or Permission not found")
        return role

    @staticmethod
    async def delete_role(role_id: int, session: AsyncSession):
        role = await authorisation_service.get_role_by_id(role_id, session)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return await authorisation_service.delete_role(role_id, session)
