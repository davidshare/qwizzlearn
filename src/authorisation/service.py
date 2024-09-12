from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from src.authentication.models import User
from src.authentication.service import AuthenticationService
from .models import Role, Permission, RolePermissions, UserRoles
from .schemas import RoleCreate, PermissionCreate, RoleUpdate, PermissionUpdate, AssignPermissionToRole, AssignRoleToUser
from .exceptions import PermissionNotFoundException, RoleNotFoundException

authentication_service = AuthenticationService()


class AuthorisationService:

    async def create_permission(self, permission_data: List[PermissionCreate], user_id: int, session: AsyncSession):
        """
        Handle creating permissions. If a permission exists, return it; if not, create it.
        """
        existing_permissions = []
        new_permissions = []

        for permission in permission_data:
            result = await session.exec(
                select(Permission).where(
                    Permission.action == permission.action)
            )
            existing_permission = result.first()

            if existing_permission:
                existing_permissions.append(existing_permission)
            else:
                new_permission = Permission(
                    **permission.model_dump(), created_by=user_id)
                new_permissions.append(new_permission)

        session.add_all(new_permissions)

        await session.commit()

        for permission in new_permissions:
            await session.refresh(permission)

        return existing_permissions + new_permissions

    async def update_permission(self, permission_id: int, permission_data: PermissionUpdate, user: User, session: AsyncSession):
        permission = await self.get_permission_by_id(permission_id, session)

        if not permission:
            raise PermissionNotFoundException("Permission not found")

        for key, value in permission_data.model_dump(exclude_unset=True).items():
            setattr(permission, key, value)

        if permission.created_by != user.id:
            permission.created_by = user.id

        await session.commit()
        await session.refresh(permission)
        return permission

    async def get_all_permissions(self, session: AsyncSession):
        statement = select(Permission)
        result = await session.exec(statement)
        return result.all()

    async def get_permission_by_id(self, permission_id: int, session: AsyncSession):
        statement = select(Permission).where(Permission.id == permission_id)
        result = await session.exec(statement)
        return result.first()

    async def get_permission_by_action(self, permission_action: str, session: AsyncSession):
        statement = select(Permission).where(
            Permission.action == permission_action)
        permission = await session.exec(statement)
        return permission.first()

    async def delete_permission(self, permission_id: int, session: AsyncSession):
        permission = await self.get_permission_by_id(permission_id, session)

        if permission:
            await session.delete(permission)
            await session.commit()
            return {"message": f"Permission {permission_id} deleted successfully."}
        return None

    async def create_role(self, role_data: RoleCreate, user: User, session: AsyncSession):
        """
        Handle creating roles. If a role  exists, return it; if not, create it.
        """
        if not user.id:
            raise ValueError("Please provide a user object with an id")

        existing_roles = []
        new_roles = []

        for role in role_data:
            result = await session.exec(
                select(Role).where(Role.name == role.name)
            )
            existing_role = result.first()

            if existing_role:
                existing_roles.append(existing_role)
            else:
                new_role = Role(
                    **role.model_dump(), created_by=user.id
                )

                new_roles.append(new_role)
        session.add_all(new_roles)
        await session.commit()

        for role in new_roles:
            await session.refresh(role)

        return existing_roles + new_roles

    async def get_all_roles(self, session: AsyncSession):
        statement = select(Role)
        result = await session.exec(statement)
        return result.all()

    async def get_role_by_id(self, role_id: int, session: AsyncSession):
        statement = select(Role).where(Role.id == role_id)
        result = await session.exec(statement)
        return result.first()

    async def get_role_by_name(self, role_name: str, session: AsyncSession):
        statement = select(Role).where(Role.name == role_name)
        result = await session.exec(statement)
        return result.first()

    async def update_role(self, role_id: int, role_data: RoleUpdate, user: User,  session: AsyncSession):
        role = await self.get_role_by_id(role_id, session)

        if not role:
            raise RoleNotFoundException("Role not found")

        for key, value in role_data.model_dump(exclude_unset=True).items():
            setattr(role, key, value)

        if role.created_by != user.id:
            role.created_by = user.id

        await session.commit()
        await session.refresh(role)
        return role

    async def delete_role(self, role_id: int, session: AsyncSession):
        statement = select(Role).where(Role.id == role_id)
        result = await session.exec(statement)
        role = result.first()

        if role:
            await session.delete(role)
            await session.commit()
            return {"message": f"Role {role_id} deleted successfully."}
        return None

    async def assign_permission_to_role(self, permissions_data: List[AssignPermissionToRole], user: User, session: AsyncSession):
        # Assuming all permissions have the same role_id
        role_id = permissions_data[0].role_id

        role = await self.get_role_by_id(role_id, session)
        if not role:
            raise RoleNotFoundException(f"Role with id {role_id} not found")

        role_permissions = []
        for permission_data in permissions_data:
            permission_id = permission_data.permission_id

            permission = await self.get_permission_by_id(permission_id, session)
            if not permission:
                raise PermissionNotFoundException(
                    f"Permission with id {permission_id} not found")

            # Check if the permission is already assigned to the role
            statement = select(RolePermissions).where(
                RolePermissions.role_id == role_id,
                RolePermissions.permission_id == permission_id
            )
            result = await session.exec(statement)
            existing_role_permission = result.first()

            if not existing_role_permission:
                # Create the RolePermissions entry
                role_permission = RolePermissions(
                    role_id=role_id,
                    permission_id=permission_id,
                    assigned_by=user.id
                )
                role_permissions.append(role_permission)
            else:
                role_permissions.append(existing_role_permission)

        try:
            if role_permissions:
                session.add_all(role_permissions)
                await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise e

        return role_permissions, None

    async def assign_roles_to_user(self, roles_data: List[AssignRoleToUser], user: User, session: AsyncSession):
        user_roles = []
        for role_data in roles_data:
            user_id = role_data.user_id
            role_id = role_data.role_id

            # Check if the role is already assigned to the user
            statement = select(UserRoles).where(
                UserRoles.user_id == user_id,
                UserRoles.role_id == role_id
            )
            result = await session.exec(statement)
            existing_user_role = result.first()

            if not existing_user_role:
                # Create the UserRoles entry
                user_role = UserRoles(
                    user_id=user_id,
                    role_id=role_id,
                    assigned_by=user.id
                )
                user_roles.append(user_role)
            else:
                user_roles.append(existing_user_role)
        try:
            if user_roles:
                session.add_all(user_roles)
                await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise e

        return user_roles, None
