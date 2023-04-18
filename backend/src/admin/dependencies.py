from fastapi import Depends
from src.authentication import AuthModel, get_token_user
from src.core.enums import UserType
from src.core.exceptions import ForbiddenException


async def get_admin_user(
    user: AuthModel = Depends(get_token_user),
) -> AuthModel:
    """Get the user if it is not deactivated and is admin.

    #### Args:
    - user (AuthModel):
        The user object from the database.

    #### Raises:
    - NotActiveUserException:
        The user is not admin.

    #### Returns:
    - AuthModel:
        The user object from the database.
    """
    if user.user_type != UserType.ADMIN:
        raise ForbiddenException

    return user
