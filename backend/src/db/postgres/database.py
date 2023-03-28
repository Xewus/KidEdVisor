import asyncpg
from asyncpg.connection import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings

engine = create_async_engine(
    url=settings.postgres_url,
    future=True,
    echo=settings.debug,
)


SessionMaker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """Get connection to the PostgresSQL."""
    async with SessionMaker() as session:
        yield session


async def check_postgres() -> None:
    """Check connection to the PostgresSQL.

    #### Raises:
    - ConnectionError:
        No connection to PostgreSQL.
    """
    try:
        dsn = settings.postgres_url.replace("+asyncpg", "")
        conn: Connection = await asyncpg.connect(dsn)
        await conn.close()
    except Exception as exc:
        raise ConnectionError(
            f"\n\n\033[101mNo connection to PostgreSQL!\n{exc}\033[0m"
        )

    return None
