import asyncpg
from asyncpg.connection import Connection
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    sessionmaker,
)

from src.config import settings
from src.core.utils import postgres_dsn


class IDTable:
    """Mixin to add `id` field to table with integer type as primary key.

    #### Attrs:
    - id (int | None):
        Primary key for table.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


postgres_url = postgres_dsn(
    user=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_port,
    db_name=settings.postgres_db_name,
)

Base = declarative_base(cls=IDTable)

aengine = create_async_engine(
    url=postgres_url,
    echo=settings.debug,
)

aengine.echo = True

ASessionMaker = sessionmaker(
    bind=aengine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """Get connection to the Postgres."""
    async with ASessionMaker() as session:
        yield session


async def check_postgres() -> None:
    """Check connection to the PostgresSQL.

    #### Raises:
    - ConnectionError:
        No connection to PostgreSQL.
    """
    try:
        dsn = postgres_url.replace("+asyncpg", "")
        conn: Connection = await asyncpg.connect(dsn)
        await conn.execute("SELECT 1;")
        await conn.close()
    except Exception as exc:
        raise ConnectionError(
            f"\n\n\033[101mNo connection to PostgreSQL!\n{exc}\033[0m"
        )

    return None
