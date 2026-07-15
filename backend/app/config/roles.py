from fastapi import HTTPException, status, Depends

from app.config.jwt import get_current_user


def require_roles(*allowed_roles):

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized."
            )

        return current_user

    return role_checker