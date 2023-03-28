from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Limits


class CRUD:
    """The set of `CRUD` operations.

    #### Methods:
    - save: tuple[SQLModel, None] | tuple[None, str]
    - create: tuple[SQLModel, None] | tuple[None, str]
    - get_many: list[SQLModel]
    - get: SQLModel | None
    - update: tuple[SQLModel, None] | tuple[None, str]
    """

    model: SQLModel

    def __init__(self, model: SQLModel) -> None:
        self.model = model

    async def save(
        self,
        db: AsyncSession,
        obj: SQLModel,
        need_refresh: bool = False,
    ) -> tuple[SQLModel, None] | tuple[None, str]:
        """Save object to database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - obj (SQLModel):
            Data to save to the database.
        - need_refresh (bool): Default False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[SQLModel, None] | tuple[None, str]:
            (SQLModel, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        db.add(obj)
        try:
            await db.commit()
        except IntegrityError as err:
            return None, err.args[0].split(".")[-1]

        if need_refresh:
            await db.refresh(obj)
        return obj, None

    async def create(
        self,
        db: AsyncSession,
        new_obj: SQLModel | dict,
        need_refresh: bool = False,
    ) -> tuple[SQLModel, None] | tuple[None, str]:
        """Create a new object in the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - new_obj (SQLModel | dict):
            Data to save to the database.
        - need_refresh (bool): Default False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[SQLModel, None] | tuple[None, str]:
            (SQLModel, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        if isinstance(new_obj, dict):
            db_obj = self.model(**new_obj)
        else:
            db_obj = self.model.from_orm(new_obj)
        return await self.save(db, db_obj, need_refresh)

    async def get_many(
        self,
        db: AsyncSession,
        offset: int | None = 0,
        limit: int | None = Limits.DEFAULT_PAGINATION_SIZE,
        expression: BinaryExpression | None = None,
    ) -> list[SQLModel]:
        """Get many objects from the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - offset (int): Default `0`.
            Skips the offset objects before beginning to return the objects.
        - limit (int): Default and maximum from ` app settings`.
            Limit the number of objects returned from a query.
        - expression (BinaryExpression): Default `None`.
            Filter expression.

        #### Returns:
        - list[SQLModel]
            List of objects.
        """
        limit = min(limit, Limits.DEFAULT_PAGINATION_SIZE)
        stmt = select(self.model).offset(offset).limit(limit)
        if expression is not None:
            stmt = stmt.where(expression)
        return (await db.exec(stmt)).all()

    async def get(
        self,
        db: AsyncSession,
        expression: BinaryExpression,
    ) -> SQLModel | None:
        """Get an object from the database by ID.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - expression (BinaryExpression):
            Filter expression.

        #### Returns:
        - SQLModel | None:
            An object if it exists in the database else None.
        """
        stmt = select(self.model).where(expression).limit(1)
        return (await db.exec(stmt)).one_or_none()

    async def update(
        self,
        db: AsyncSession,
        obj: SQLModel,
        update_data: dict,
        need_refresh: bool = False,
    ) -> tuple[SQLModel, None] | tuple[None, str]:
        """Update object in the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - obj (SQLModel):
            Object in database.
        - update_data (dict):
            Data for update.
        - need_refresh (bool): Default False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[SQLModel, None] | tuple[None, str]:
            (SQLModel, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        is_update = False
        for key, value in update_data.items():
            if key in obj.__fields__:
                is_update = True
                setattr(obj, key, value)
        if not is_update:
            return obj, None

        db.add(obj)
        return await self.save(db, obj, need_refresh)
