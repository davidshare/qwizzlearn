from typing import Optional, List
from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    created_by: int  # This field tracks the user who created the role


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_by: int  # User ID who created this role

    class Config:
        orm_mode = True


class AssignRoleToUser(BaseModel):
    user_id: int
    role_id: int
    assigned_by: int  # Track which user assigned this role


class UserRolesResponse(BaseModel):
    user_id: int
    roles: List[RoleResponse]

    class Config:
        orm_mode = True


class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    created_by: int  # This tracks the user who created the permission


class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_by: int  # User ID who created this permission

    class Config:
        orm_mode = True


class AssignPermissionToRole(BaseModel):
    role_id: int
    permission_id: int
    assigned_by: int  # Track which user assigned the permission


class RolePermissionsResponse(BaseModel):
    role_id: int
    permissions: List[PermissionResponse]

    class Config:
        orm_mode = True


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
