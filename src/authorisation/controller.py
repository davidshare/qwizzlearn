from typing import List
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.models import User
from .schemas import RoleCreate, PermissionCreate, RoleUpdate, PermissionUpdate, AssignPermissionToRole, AssignRoleToUser
from .service import AuthorisationService
from .exceptions import PermissionNotFoundException, RoleNotFoundException
from .validators import AuthorisationValidator

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
    async def delete_role(role_id: int, session: AsyncSession):
        if not role_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role ID missing: please provide the id of the role."
            )
        try:
            return await authorisation_service.delete_role(role_id, session)
        except RoleNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found") from e

    @staticmethod
    async def assign_permissions_to_role(permissions_data: List[AssignPermissionToRole], user: User, session: AsyncSession):
        for permission in permissions_data:
            if not permission.role_id or not permission.permission_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Please both the role_id and permission_id are required"
                )
        if not user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is missing. You need a valid user to create permissions."
            )

        try:
            role_permissions = await authorisation_service.assign_permission_to_role(permissions_data, user, session)
        except RoleNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found") from e
        except PermissionNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found") from e
        return role_permissions

    @staticmethod
    async def assign_roles_to_user(roles_data: List[AssignRoleToUser], user: User, session: AsyncSession):
        for role_data in roles_data:
            if not role_data.user_id or not role_data.role_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Both user_id and role_id are required"
                )
            if not user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User ID is missing. You need a valid user to assign roles."
                )
        await AuthorisationValidator.validate_users_and_roles(roles_data, session)
        user_roles, error = await authorisation_service.assign_roles_to_user(roles_data, user, session)

        if error == "UserNotFound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        elif error == "RoleNotFound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        elif error == "IntegrityError":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more roles are already assigned to the user"
            )

        return user_roles

    @staticmethod
    async def revoke_user_roles(user_id: int, role_ids: List[int], session: AsyncSession):
        if not role_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role IDs are required"
            )

        user_roles, error = await authorisation_service.revoke_user_roles(user_id, role_ids, session)

        if error == "RolesNotFound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more roles not found for the user"
            )
        elif error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An error occurred while revoking roles"
            )

        return user_roles
