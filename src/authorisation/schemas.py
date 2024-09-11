from typing import Optional, List
from pydantic import BaseModel


class RoleCreate(BaseModel):
    """
    Schema for creating a new role.
    """
    name: str
    description: Optional[str] = None
    created_by: int  # ID of the user who created the role


class RoleResponse(BaseModel):
    """
    Response schema for a role.
    """
    id: int
    name: str
    description: Optional[str]
    created_by: Optional[int]  # Creator might be optional in the response

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
    roles: List[RoleResponse]  # A list of roles the user has been assigned

    class Config:
        """
        Map to orm models
        """
        from_attributes = True


class PermissionCreate(BaseModel):
    """
    Schema for creating a new permission.
    """
    name: str
    description: Optional[str] = None
    created_by: int  # ID of the user who created the permission


class PermissionResponse(BaseModel):
    """
    Response schema for a permission.
    """
    id: int
    name: str
    description: Optional[str]
    created_by: Optional[int]  # Creator might be optional in the response

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
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionUpdate(BaseModel):
    """
    Schema for updating a permission.
    """
    name: Optional[str] = None
    description: Optional[str] = None
