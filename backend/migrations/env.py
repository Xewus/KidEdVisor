import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config

BASE_ROOT = Path(__file__).parent.parent.parent
sys.path.append(BASE_ROOT)

from src.authentication import AuthModel
from src.core.utils import postgres_dsn
from src.db.postgres.database import Base
from src.geo import (
    AddressModel,
    CityModel,
    CountryModel,
    PhoneModel,
    RegionModel,
    StreetModel,
)
from src.parents import ParentModel
from src.providers import (
    CategoryModel,
    InstitutionModel,
    OwnerModel,
    TeacherModel,
)

load_dotenv(BASE_ROOT / ".env")

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_NAME = os.environ.get("POSTGRES_NAME")

postgres_url = postgres_dsn(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    db_name=POSTGRES_NAME,
)
config = context.config
config.set_main_option("sqlalchemy.url", postgres_url)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(connectable: AsyncEngine):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = context.config.attributes.get("connection", None)
    connectable: AsyncEngine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    if isinstance(connectable, AsyncEngine):
        asyncio.run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


run_migrations_online()
