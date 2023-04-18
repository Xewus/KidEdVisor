from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from src.config import Limits, RedisPrefixes
from src.db.postgres import CRUD
from src.db.redis import auth_db

from .models import AuthModel, TempUserModel
from .schemes import CreateTempUserScheme


class TempCRUD:
    """The set of `CRUD` operations for `TempUserModel`.

    #### Methods:
    - set: str
    - pop: TempUserModel | None
    """

    expiire = Limits.CONFIRM_EXPIRE_TIME
    model = TempUserModel
    prefix_temp_user = RedisPrefixes.TEMP_USER
    prefix_newpassword = RedisPrefixes.NEWPASSWORD

    def __set_temp_data(self, data: Any, prefix: str) -> str:
        """Put data in temporary storage.

        #### Args:
        - data (Any):
            Storage data.
        - prefix (str):
            Namespace.

        #### Returns:
        - str:
            UUID key to get data from temporary storage
        """
        uuid = uuid4().hex
        name = prefix + uuid
        auth_db.set(
            name,
            data,
            self.expiire,
        )
        return uuid

    def set_temp_user(self, user: CreateTempUserScheme) -> str:
        """Put user data in temporary storage.

        #### Args:
        - user (CreateTempUserScheme):
            New user data.

        #### Returns:
        - str:
            UUID key to get user data from temporary storage.
        """
        value = user.json(exclude_none=True)
        return self.__set_temp_data(value, self.prefix_temp_user)

    def set_want_password(self, email: str) -> str:
        """Put user data in temporary storage.

        #### Args:
        - email (str):
            Email address.

        #### Returns:
        - str:
            UUID key to get email address from temporary storage.
        """
        return self.__set_temp_data(email, self.prefix_newpassword)

    def pop_temp_user(self, uuid: str) -> TempUserModel | None:
        """Get user data from temporary storage and delete from storage.

        #### Args:
        - uuid (str):
            UUID key to get user data.

        #### Returns:
        - TempUserModel | None:
            User data if it exists.
        """
        name = self.prefix_temp_user + uuid
        temp_user = auth_db.get(name)
        if temp_user is None:
            return None

        auth_db.delete(name)
        return self.model.parse_raw(temp_user)

    def pop_want_password(self, uuid: str) -> str | None:
        """Get email from temporary storage and delete from storage.

        #### Args:
        - uuid (str):
            UUID key to get user data.

        #### Returns:
        - str | None:
            User data if it exists.
        """
        name = self.prefix_newpassword + uuid
        email: bytes = auth_db.get(name)
        if email is None:
            return None

        auth_db.delete(name)
        return email.decode()


class AuthCrud(CRUD):
    """The set of `CRUD` operations for `AuthModel`.

    #### Methods:
    - save: tuple[AuthModel, None] | tuple[None, str]
    - create: tuple[AuthModel, None] | tuple[None, str]
    - get_many: list[AuthModel]
    - get: AuthModel | None
    - update: tuple[AuthModel, None] | tuple[None, str]
    - email_exists: bool
    """

    model: AuthModel

    async def create(
        self,
        db: AsyncSession,
        new_obj: dict,
        is_active: bool = False,
        need_refresh: bool = False,
    ) -> tuple[AuthModel, None] | tuple[None, str]:
        """Create a new object in the table.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - new_obj (dict):
            User data to save to the database.
        - is_active (bool): Default False.
            Is the user activated.
        - need_refresh (bool): Default False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[AuthUserModel, None] | tuple[None, str]:
            (AuthModel, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        db_obj: AuthModel = self.model(**new_obj)
        db_obj.is_active = is_active
        return await self.save(db, db_obj, need_refresh)

    async def email_exists(
        self,
        db: AsyncSession,
        email: str,
    ) -> bool:
        """Exists is there an email in the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - email (str):
            Search email.

        #### Returns:
        - bool:
            Exists or not.
        """
        return await self.get(db, self.model.email == email) is not None


auth_crud = AuthCrud(AuthModel)
temp_crud = TempCRUD()
