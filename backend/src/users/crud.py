from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.models import AuthModel
from src.core.enums import UserType
from src.core.exceptions import ServerError
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
    - get_by_email: ParentModel | str
    - get_with_auth_by_email: tuple[ParentModel, AuthModel] | None
    - delete_auth: None
    """

    model: ParentModel

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
        is_active: bool | None = None,
    ) -> ParentModel | None:
        """Get `parent` by `auth` email.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - email (str):
            User's email as identifier.
        - is_active (bool | None): Default `None`.
            Use filter by `is_active` field.

        #### Returns:
        - ParentModel | None:
            User data if it exists.
        """
        stmt = (
            select(ParentModel)
            .join(AuthModel)
            .where(
                AuthModel.email == email,
                AuthModel.user_type == UserType.PARENT,
            )
            .limit(1)
        )
        if is_active is not None:
            stmt = stmt.where(AuthModel.is_active == is_active)
        return (await db.exec(stmt)).one_or_none()

    async def get_with_auth_by_email(
        self,
        db: AsyncSession,
        email: str,
        is_active: bool | None = None,
    ) -> tuple[ParentModel, AuthModel] | None:
        """Get 'parent' and 'auth' tables by email.

        On the first call, a record is created in the table `parent`.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - email (str):
            User's email as identifier.
        - is_active (bool | None): Default `None`.
            Use filter by `is_active` field.

        #### Raises:
        - ServerError:
            Failed to create data in 'parent' table.

        #### Returns:
        - tuple[ParentModel, AuthModel] | None:
            User data and auth data if it exists.
        """
        stmt = (
            select(ParentModel, AuthModel)
            .outerjoin(ParentModel)
            .where(
                AuthModel.email == email,
                AuthModel.user_type == UserType.PARENT,
            )
            .limit(1)
        )
        if is_active is not None:
            stmt = stmt.where(AuthModel.is_active == is_active)
        # returns (ParentModel, AuthModel) #
        parent_auth = (await db.exec(stmt)).one_or_none()
        if parent_auth is None:
            return None

        parent, auth = parent_auth
        if parent is None:
            parent, err = await self.create(
                db=db,
                new_obj={"auth_id": auth.id},
                need_refresh=True,
            )
            if err is not None:
                raise ServerError("can't create profile")

        return parent, auth

    async def delete_auth(
        self,
        db: AsyncSession,
        auth_user: AuthModel,
    ) -> None:
        """Set `parent.auth_id` to None and remove the related `auth` object.

        A user without `auth` cannot use the application,
        but an administrator can use with purpose of analytics.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - auth_user (AuthModel):
            `auth` object for delete.
        """
        await db.exec(
            update(ParentModel)
            .where(ParentModel.auth_id == auth_user.id)
            .values({ParentModel.auth_id: None})
        )
        await db.delete(auth_user)
        await db.commit()
        return None


parent_crud = ParentCRUD(ParentModel)
