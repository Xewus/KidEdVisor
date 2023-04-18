from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.authentication.schemes import TokenDataScheme
from src.authentication.security import get_token_data
from src.core.exceptions import CredentialsException, ForbiddenException
from src.db.postgres import get_db

from .owners.crud import owner_crud
from .owners.models import OwnerModel


async def get_token_empty_owner(
    db: AsyncSession = Depends(get_db),
    token_data: TokenDataScheme = Depends(get_token_data),
) -> OwnerModel:
    """Get owner by `JWT` token.

    #### Args:
    - db (AsyncSession):
        Connecting to the database.
    - token_data (TokenDataScheme):
        Data from JWT token.

    #### Raises:
    - CredentialsException:
        The token is invalid or owner is not active.

    #### Returns:
    - OwnerModel:
        The owner object.
    """
    owner = await owner_crud.get_active_owner(db, token_data.email)
    if owner is None:
        raise CredentialsException

    return owner


async def get_token_owner(
    active_owner: OwnerModel = Depends(get_token_empty_owner),
) -> OwnerModel:
    """Get owner by `JWT` token.

    #### Args:
    - db (AsyncSession):
        Connecting to the database.
    - active_owner (OwnerModel):
        Active owner.

    #### Raises:
    - ForbiddenException:
        Owner profile is empty.

    #### Returns:
    - OwnerModel:
        The owner object.
    """
    if not all(active_owner.__dict__.values()):
        raise ForbiddenException("please, fill your profile first")
    return active_owner
