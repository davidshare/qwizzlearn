from typing import Callable
from fastapi import Depends, HTTPException, Request
from src.authentication.dependencies import get_current_user
from src.authentication.models import User


def route_with_action(action: str):
    def decorator(func: Callable):
        func.action = action
        return func
    return decorator


async def authorize(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    route = request.scope.get("route")
    if not route or not hasattr(route.endpoint, "action"):
        raise HTTPException(status_code=500, detail="Route action not defined")

    action = route.endpoint.action

    user_permissions = set()
    for role in current_user.roles:
        for permission in role.permissions:
            user_permissions.add((permission.action, permission.is_owner_only))

    for perm_action, is_owner_only in user_permissions:
        if perm_action == action:
            if is_owner_only:
                owner_id = request.path_params.get("user_id")
                if owner_id is None:
                    raise HTTPException(
                        status_code=400, detail="Owner ID not found in the path")

                if not check_ownership(current_user.id, owner_id):
                    raise HTTPException(
                        status_code=403, detail="Not authorized - you are not the owner of this resource")

            return True

    raise HTTPException(
        status_code=403, detail="Not authorized: You don't have the permission to access this result. Please contact your admin.")


def check_ownership(user_id: int, owner_id: str) -> bool:
    return str(user_id) == owner_id
