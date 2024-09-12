from .authorisation.models import Role, Permission, RolePermissions, UserRoles
from .authentication.models import User


# Update forward references
User.model_rebuild()
Role.model_rebuild()
Permission.model_rebuild()

# This ensures all models are imported and can be referenced
__all__ = ["User", "UserRoles", "RolePermissions", "Role", "Permission"]
