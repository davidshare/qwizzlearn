from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.authentication.models import User
from .models import Role, Permission
from .schemas import RoleCreate, PermissionCreate, RoleUpdate, PermissionUpdate
from .exceptions import PermissionNotFoundException


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

    async def create_role(self, role_data: RoleCreate, session: AsyncSession):
        new_role = Role(**role_data.model_dump())
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)
        return new_role

    async def assign_permission_to_role(self, role_id: int, permission_id: int, session: AsyncSession):
        statement = select(Role).where(Role.id == role_id)
        result = await session.exec(statement)
        role = result.first()

        statement = select(Permission).where(Permission.id == permission_id)
        result = await session.exec(statement)
        permission = result.first()

        if role and permission:
            permission.role_id = role_id
            await session.commit()
            return role
        else:
            return None

    async def get_role(self, role_id: int, session: AsyncSession):
        statement = select(Role).where(Role.id == role_id)
        result = await session.exec(statement)
        return result.first()

    async def get_role_by_name(self, role_name: str, session: AsyncSession):
        statement = select(Role).where(Role.name == role_name)
        result = await session.exec(statement)
        return result.first()

    async def role_exist(self, role_name: str, session: AsyncSession):
        if not role_name:
            raise ValueError(
                "Please provide the role name")

        role = self.get_role_by_name(role_name, session)
        return role is not None

    async def get_all_roles(self, session: AsyncSession):
        statement = select(Role)
        result = await session.exec(statement)
        return result.all()

    async def update_role(self, role_id: int, role_data: RoleUpdate, session: AsyncSession):
        statement = select(Role).where(Role.id == role_id)
        result = await session.exec(statement)
        role = result.first()

        if role:
            for key, value in role_data.model_dump(exclude_unset=True).items():
                setattr(role, key, value)

            await session.commit()
            await session.refresh(role)
            return role
        return None

    async def delete_role(self, role_id: int, session: AsyncSession):
        statement = select(Role).where(Role.id == role_id)
        result = await session.exec(statement)
        role = result.first()

        if role:
            await session.delete(role)
            await session.commit()
            return {"message": f"Role {role_id} deleted successfully."}
        return None
