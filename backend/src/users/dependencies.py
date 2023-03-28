from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.models import AuthModel
from src.authentication.schemes import TokenDataScheme
from src.authentication.security import get_token_data
from src.core.exceptions import CredentialsException
from src.db.postgres.database import get_db

from .crud import parent_crud
from .models import ParentModel


async def get_token_parent_auth(
    db: AsyncSession = Depends(get_db),
    token_data: TokenDataScheme = Depends(get_token_data),
) -> tuple[ParentModel, AuthModel]:
    """Get parent by `JWT` token. Extended by `AuthModel`.

    #### Args:
    - db (AsyncSession):
        Connecting to the database.
    - token_data (TokenDataScheme):
        Data from JWT token.

    #### Raises:
    - CredentialsException:
        The token is invalid.

    #### Returns:
    - tuple[ParentModel, AuthModel]:
        The parent and auth objects.
    """
    parent_auth = await parent_crud.get_with_auth_by_email(
        db, token_data.email, True
    )
    if parent_auth is None:
        raise CredentialsException

    return parent_auth
