from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import Role, Permission
from .schemas import RoleCreate, PermissionCreate, RoleUpdate, PermissionUpdate


class RolePermissionService:

    async def create_role(self, role_data: RoleCreate, session: AsyncSession):
        new_role = Role(**role_data.model_dump())
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)
        return new_role

    async def create_permission(self, permission_data: PermissionCreate, session: AsyncSession):
        new_permission = Permission(**permission_data.model_dump())
        session.add(new_permission)
        await session.commit()
        await session.refresh(new_permission)
        return new_permission

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

    async def get_permission(self, permission_id: int, session: AsyncSession):
        statement = select(Permission).where(Permission.id == permission_id)
        result = await session.exec(statement)
        return result.first()

    async def get_all_roles(self, session: AsyncSession):
        statement = select(Role)
        result = await session.exec(statement)
        return result.all()

    async def get_all_permissions(self, session: AsyncSession):
        statement = select(Permission)
        result = await session.exec(statement)
        return result.all()
    # Existing methods...

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

    async def update_permission(self, permission_id: int, permission_data: PermissionUpdate, session: AsyncSession):
        statement = select(Permission).where(Permission.id == permission_id)
        result = await session.exec(statement)
        permission = result.first()

        if permission:
            for key, value in permission_data.model_dump(exclude_unset=True).items():
                setattr(permission, key, value)

            await session.commit()
            await session.refresh(permission)
            return permission
        return None

    async def delete_permission(self, permission_id: int, session: AsyncSession):
        statement = select(Permission).where(Permission.id == permission_id)
        result = await session.exec(statement)
        permission = result.first()

        if permission:
            await session.delete(permission)
            await session.commit()
            return {"message": f"Permission {permission_id} deleted successfully."}
        return None
