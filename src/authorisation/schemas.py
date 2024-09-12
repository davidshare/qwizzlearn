from typing import Optional, List
from pydantic import BaseModel


class PermissionCreate(BaseModel):
    """
    Schema for creating a new permission.
    """
    action: str
    is_owner_only: Optional[bool] = False
    description: Optional[str] = None


class PermissionUpdate(BaseModel):
    """
    Schema for updating a permission.
    """
    action: Optional[str] = None
    is_owner_only: Optional[bool] = False
    description: Optional[str] = None
    created_by: Optional[int] = None


class PermissionResponse(BaseModel):
    """
    Response schema for a permission.
    """
    id: int
    action: str
    is_owner_only: Optional[bool] = False
    description: Optional[str]
    created_by: Optional[int]  # Creator might be optional in the response

    class Config:
        """
        Map to orm models
        """
        from_attributes = True


class RoleCreate(BaseModel):
    """
    Schema for creating a new role.
    """
    action: str
    description: Optional[str] = None
    created_by: int  # ID of the user who created the role


class RoleResponse(BaseModel):
    """
    Response schema for a role.
    """
    id: int
    action: str
    description: Optional[str]
    created_by: Optional[int]

    class Config:
        """
        Map to orm models
        """
        from_attributes = True  # Use this if you're using ORM models


class AssignRoleToUser(BaseModel):
    """
    Schema for assigning a role to a user.
    """
    user_id: int
    role_id: int
    assigned_by: int  # Track the user who performed the assignment


class UserRolesResponse(BaseModel):
    """
    Response schema for the roles of a user.
    """
    user_id: int
    roles: List[RoleResponse] = []

    class Config:
        """
        Map to orm models
        """
        from_attributes = True


class AssignPermissionToRole(BaseModel):
    """
    Schema for assigning a permission to a role.
    """
    role_id: int
    permission_id: int
    assigned_by: int  # Track the user who performed the assignment


class RolePermissionsResponse(BaseModel):
    """
    Response schema for the permissions of a role.
    """
    role_id: int
    permissions: List[PermissionResponse]  # A list of permissions the role has

    class Config:
        """
        Map to orm models
        """
        from_attributes = True


class RoleUpdate(BaseModel):
    """
    Schema for updating a role.
    """
    action: Optional[str] = None
    description: Optional[str] = None
