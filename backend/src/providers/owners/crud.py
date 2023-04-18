from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.authentication import AuthModel
from src.db.postgres import CRUD

from .models import OwnerAddressModel, OwnerModel


class OwnerCRUD(CRUD):
    """The set of `CRUD` operations for `OwnerModel`.

    #### Methods:
    - save: tuple[Base, None] | tuple[None, str]
    - create: tuple[Base, None] | tuple[None, str]
    - get_many: list[Base]
    - get: Base | None
    - update: tuple[Base, None] | tuple[None, str]
    """

    model: OwnerModel

    async def get_active_owner(
        self,
        db: AsyncSession,
        email: str,
    ) -> OwnerModel | None:
        return await db.scalar(
            select(self.model)
            .join(AuthModel, self.model.auth_id == AuthModel.id)
            .where(
                AuthModel.email == email,
                AuthModel.is_active == True,  # noqa E712
            )
            .limit(1)
        )

    async def delete_auth(
        self,
        db: AsyncSession,
        email: str,
    ) -> None:
        """Remove the corresponding `auth` object.

        A user without `auth` cannot use the application,
        but an administrator can use with purpose of analytics.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - email (str):
            The email to look for the `auth` object to delete.
        """
        await db.execute(delete(AuthModel).where(AuthModel.email == email))
        await db.commit()
        return None


class OwnerAddressCRUD(CRUD):
    model: OwnerAddressModel


owner_crud = OwnerCRUD(OwnerModel)
owner_addres_crud = CRUD(OwnerAddressModel)
