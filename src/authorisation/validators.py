from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.authentication.models import User

from .models import Role


class AuthorisationValidator:
    @staticmethod
    async def validate_users_and_roles(data: List[Dict[str, int]], session: AsyncSession):
        # Extract unique user_ids and role_ids
        print("=========================================>>>>>>>>>>>> data: ", data)
        user_ids = list(set(item.user_id for item in data))
        role_ids = list(set(item.role_id for item in data))

        # Query existing users
        existing_users_result = await session.exec(select(User).where(
            or_(*[User.id == id for id in user_ids])))
        existing_users = existing_users_result.all()
        existing_user_ids = set(user.id for user in existing_users)

        # Query existing roles
        existing_roles_result = await session.exec(select(Role).where(
            or_(*[Role.id == id for id in role_ids])))
        existing_roles = existing_roles_result.all()
        existing_role_ids = set(role.id for role in existing_roles)

        # Find non-existent users and roles
        non_existent_users = set(user_ids) - existing_user_ids
        non_existent_roles = set(role_ids) - existing_role_ids

        # Prepare error message if there are any non-existent users or roles
        if non_existent_users or non_existent_roles:
            error_msg = "Validation failed. "
            if non_existent_users:
                error_msg += f"Non-existent user IDs: {list(non_existent_users)}. "
            if non_existent_roles:
                error_msg += f"Non-existent role IDs: {list(non_existent_roles)}."
            raise HTTPException(status_code=400, detail=error_msg)

        return existing_users, existing_roles