from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.authentication.models import AuthModel
from src.db.postgres.crud import CRUD

from .models import ParentModel


class ParentCRUD(CRUD):
    """The set of `CRUD` operations for `ParentModel`.

    #### Methods:
    - save: tuple[ParentModel, None] | tuple[None, str]
    - create: tuple[ParentModel, None] | tuple[None, str]
    - get_many: list[ParentModel]
    - get: ParentModel | None
    - update: tuple[ParentModel, None] | tuple[None, str]
    get_active_parent: ParentModel | None
    - delete_auth: None
    """

    model: ParentModel

    async def get_active_parent(
        self, db: AsyncSession, email: str
    ) -> ParentModel | None:
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


parent_crud = ParentCRUD(ParentModel)
