from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression
from src.config import Limits
from src.db.postgres.database import Base


class CRUD:
    """The set of `CRUD` operations.

    #### Methods:
    - save: tuple[Base, None] | tuple[None, str]
    - create: tuple[Base, None] | tuple[None, str]
    - get_many: list[Base]
    - get: Base | None
    - update: tuple[Base, None] | tuple[None, str]
    """

    model: Base

    def __init__(self, model: Base) -> None:
        self.model = model

    async def save(
        self,
        db: AsyncSession,
        obj: Base,
        need_refresh: bool = False,
    ) -> tuple[Base, None] | tuple[None, str]:
        """Save object to database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - obj (Base):
            Data to save to the database.
        - need_refresh (bool): Default False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[Base, None] | tuple[None, str]:
            (Base, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        db.add(obj)
        try:
            await db.commit()
        except IntegrityError as err:
            return None, err.args[0].split(":")[1]

        if need_refresh:
            await db.refresh(obj)
        return obj, None

    async def create(
        self,
        db: AsyncSession,
        new_obj: dict,
        need_refresh: bool = False,
    ) -> tuple[Base, None] | tuple[None, str]:
        """Create a new object in the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - new_obj (dict):
            Data to save to the database.
        - need_refresh (bool): Default False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[Base, None] | tuple[None, str]:
            (Base, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        db_obj = self.model(**new_obj)
        return await self.save(db, db_obj, need_refresh)

    async def get_many(
        self,
        db: AsyncSession,
        offset: int | None = 0,
        limit: int | None = Limits.DEFAULT_PAGINATION_SIZE,
        expression: BinaryExpression | None = None,
    ) -> list[Base]:
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
        - list[Base]
            List of objects.
        """
        limit = min(limit, Limits.DEFAULT_PAGINATION_SIZE)
        stmt = select(self.model).offset(offset).limit(limit)
        if expression is not None:
            stmt = stmt.where(expression)
        return (await db.scalars(stmt)).all()

    async def get(
        self,
        db: AsyncSession,
        expression: BinaryExpression,
    ) -> Base | None:
        """Get an object from the database by ID.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - expression (BinaryExpression):
            Filter expression.

        #### Returns:
        - Base | None:
            An object if it exists in the database else None.
        """
        return await db.scalar(select(self.model).where(expression).limit(1))

    async def update(
        self,
        db: AsyncSession,
        obj: Base,
        update_data: dict,
        need_refresh: bool = False,
    ) -> tuple[Base, None] | tuple[None, str]:
        """Update object in the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - obj (Base):
            Object in database.
        - update_data (dict):
            Data for update.
        - need_refresh (bool): Default False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[Base, None] | tuple[None, str]:
            (Base, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        await db.execute(
            update(self.model)
            .where(self.model.id == obj.id)
            .values(update_data)
        )
        await db.commit()
        if not need_refresh:
            return obj, None

        await db.refresh(obj)
        return obj, None
