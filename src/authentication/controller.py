from datetime import datetime, timedelta
from typing import List
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from src.authorisation.schemas import RoleResponse
from .schemas import UserCreate, UserRead, UserLogin
from .service import AuthenticationService
from .utils import verify_password, create_access_token
from .dependencies import RefreshTokenBearer, AccessTokenBearer

REFRESH_TOKEN_EXPIRY = 2
authentication_service = AuthenticationService()


class AuthenticationController:
    """
        Authentication controller
    """
    @staticmethod
    async def register(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:
        """
        Register a new user.

        This method performs the following steps:
        1. Checks if a user with the given email or username already exists.
        2. If no existing user is found, creates a new user with the provided details.
        3. Retrieves the roles associated with the newly created user.
        4. Returns the newly created user details along with their roles.

        Args:
            user (UserCreate): The user details including username, email, phone, and password.
            session (AsyncSession, optional): The database session to use for the operation. 
                If not provided, it is obtained from the dependency `get_session`.

        Returns:
            UserRead: The newly created user details including ID, username, email, 
                      email verification status, and roles.

        Raises:
            HTTPException: 
                - If a user with the same email already exists (HTTP 403 Forbidden).
                - If a user with the same username already exists (HTTP 403 Forbidden).
                - If an unexpected error occurs during user creation or role retrieval (HTTP 500 Internal Server Error).
        """
        try:
            # Check if a user with the given email or username exists
            existence = await authentication_service.user_exist(session, email=user.email, username=user.username)

            if existence.get('email'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists"
                )

            if existence.get('username'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="User with this username already exists"
                )

            # Create a new user if no existing user with the same email or username
            new_user = await authentication_service.create_user(user, session)

            new_user_dict = new_user.model_dump()
            return UserRead(**new_user_dict)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(
                    e)) from e

    @staticmethod
    async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)) -> JSONResponse:
        """
        Log in a user and return authentication tokens.

        Verifies the user's credentials and generates access and refresh tokens if valid.

        Args:
            login_data (UserLogin): User login credentials including email and password.
            session (AsyncSession): The database session to use for the operation.

        Returns:
            JSONResponse: Contains a success message, access token, refresh token,
                           and user details (email and id).

        Raises:
            HTTPException: If the email or password is incorrect.
        """
        email = login_data.email
        password = login_data.password
        user = await authentication_service.get_user_by_email(email, session)

        if user is not None:
            valid_pass = verify_password(password, user.password_hash)

            if valid_pass:
                access_token = create_access_token(
                    user_data={
                        'email': user.email,
                        'id': user.id,
                        'role': user.roles
                    }
                )

                refresh_token = create_access_token(
                    user_data={
                        'email': user.email,
                        'id': user.id
                    },
                    refresh=True,
                    expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))

                return JSONResponse(
                    content={
                        "message": "Login Successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": {
                            "email": user.email,
                            "id": user.id
                        }
                    }
                )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password."
        )

    @staticmethod
    def refresh_token(token_details: dict = Depends(RefreshTokenBearer())) -> JSONResponse:
        """
        Refresh the access token using a valid refresh token.

        Checks if the provided refresh token is valid and not expired. If valid,
        generates a new access token.

        Args:
            token_details (dict): Token details obtained from the RefreshTokenBearer dependency.

        Returns:
            JSONResponse: Contains the new access token.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        expiry_timestamp = token_details["exp"]

        if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
            new_access_token = create_access_token(
                user_data=token_details["user"]
            )

            return JSONResponse(content={"access_token": new_access_token})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    @staticmethod
    async def get_user_roles(user_id: int, session: AsyncSession) -> List[RoleResponse]:
        """
        Retrieve the roles for a specific user.

        Args:
            user_id (int): The ID of the user whose roles are to be retrieved.
            session (AsyncSession): The database session to use for the operation.

        Returns:
            List[RoleResponse]: A list of roles associated with the user.
        """
        return await authentication_service.get_user_roles(user_id, session)

    @staticmethod
    async def logout(token_details: dict = Depends(AccessTokenBearer())) -> JSONResponse:
        """
        Log out the current user by invalidating their access token.

        Adds the token identifier to the blocklist to prevent further use.

        Args:
            token_details (dict): Token details obtained from the AccessTokenBearer dependency.

        Returns:
            JSONResponse: Contains a success message and status code.
        """
        jti = token_details["jti"]
        await add_jti_to_blocklist(jti)

        return JSONResponse(
            content={
                "message": "Logged out successfully!",
                "status": status.HTTP_200_OK
            }
        )
