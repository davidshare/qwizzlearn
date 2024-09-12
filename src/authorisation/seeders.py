from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.authentication.schemas import UserCreate
from src.authorisation.models import Permission, Role, RolePermissions, UserRoles
from src.config import Config
from src.authentication.service import AuthenticationService
from src.authorisation.service import AuthorisationService
from src.db.main import get_session, AsyncSessionWrapper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Seeder:
    def __init__(self, authentication_service: AuthenticationService, authorisation_service: AuthorisationService):
        self.authentication_service = authentication_service
        self.authorisation_service = authorisation_service

    async def create_default_user(self, session: AsyncSessionWrapper) -> UserCreate:
        user_exists = await self.authentication_service.user_exist(email=Config.INITIAL_EMAIL, session=session)

        if not user_exists.get('email', False):
            user = UserCreate(
                username=Config.INITIAL_USER,
                email=Config.INITIAL_EMAIL,
                email_verified=True,
                phone=None,
                phone_verified=False,
                password=Config.INITIAL_PASSWORD,
                is_active=True
            )
            return await self.authentication_service.create_user(user, session)
        return await self.authentication_service.get_user_by_email(Config.INITIAL_EMAIL, session)

    async def create_default_roles(self, session: AsyncSession) -> Role:
        system_admin_role = await self.authorisation_service.get_role_by_name('system_admin', session)
        if not system_admin_role:
            user = await self.authentication_service.get_user_by_email(Config.INITIAL_EMAIL, session)
            system_admin_role = Role(
                name='system_admin',
                description='System Administrator role with all permissions',
                created_by=user.model_dump().get("id", None)
            )
            system_admin_role = await self.authorisation_service.create_role(system_admin_role, session)
        return system_admin_role

    async def create_default_permission(self, session: AsyncSession) -> Permission:
        all_permission = await self.authorisation_service.get_permission_by_name('all', session)
        if not all_permission:
            user = await self.authentication_service.get_user_by_email(Config.INITIAL_EMAIL, session)
            all_permission = Permission(
                name='all',
                action='all',
                is_owner_only=True,
                created_by=user.model_dump().get("id", None)
            )
            all_permission = await self.authorisation_service.create_permission(all_permission, session)
        return all_permission

    async def assign_all_permission_to_system_admin(self, session: AsyncSession) -> None:
        system_admin_role = await self.authorisation_service.get_role_by_name("system_admin", session)
        all_permission = await self.authorisation_service.get_permission_by_name("all", session)

        if not system_admin_role or not all_permission:
            raise ValueError(
                "Role 'system_admin' or Permission 'all' not found.")

        role_permission_exists = await session.exec(
            select(RolePermissions)
            .where(RolePermissions.role_id == system_admin_role.id)
            .where(RolePermissions.permission_id == all_permission.id)
        )
        if not role_permission_exists.first():
            role_perm = RolePermissions(
                role_id=system_admin_role.id,
                permission_id=all_permission.id
            )
            session.add(role_perm)
            await session.commit()

    async def seed(self):
        async with get_session() as session:
            async with session.begin():
                try:
                    user = await self.create_default_user(session)
                    role = await self.create_default_roles(session)
                    permission = await self.create_default_permission(session)
                    await self.assign_all_permission_to_system_admin(session)

                    user_role_exists = await session.exec(
                        select(UserRoles)
                        .where(UserRoles.user_id == user.id)
                        .where(UserRoles.role_id == role.id)
                    )
                    if not user_role_exists.first():
                        user_role = UserRoles(
                            user_id=user.id,
                            role_id=role.id
                        )
                        session.add(user_role)

                    logger.info("Seeding completed successfully.")
                except Exception as e:
                    logger.error(f"An error occurred during seeding: {str(e)}")
                    raise


if __name__ == "__main__":
    import asyncio

    authentication_service = AuthenticationService()
    authorisation_service = AuthorisationService()
    seeder = Seeder(authentication_service, authorisation_service)

    asyncio.run(seeder.seed())
