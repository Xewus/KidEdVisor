from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.authentication.schemes import TokenDataScheme
from src.authentication.security import get_token_data
from src.core.exceptions import CredentialsException
from src.db.postgres.database import get_db

from .parents.crud import parent_crud
from .parents.models import ParentModel


async def get_token_parent(
    db: AsyncSession = Depends(get_db),
    token_data: TokenDataScheme = Depends(get_token_data),
) -> ParentModel:
    """Get parent by `JWT` token.

    #### Args:
    - db (AsyncSession):
        Connecting to the database.
    - token_data (TokenDataScheme):
        Data from JWT token.

    #### Raises:
    - CredentialsException:
        The token is invalid or parent is not active.

    #### Returns:
    - ParentModel:
        The parent objects.
    """
    parent = await parent_crud.get_active_parent(db, token_data.email)
    if parent is None:
        raise CredentialsException
    return parent
