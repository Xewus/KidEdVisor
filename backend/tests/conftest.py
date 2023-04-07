import os
import sys

assert (sys.version_info.major, sys.version_info.minor) == (
    3,
    11,
), "Only Python 3.11 allowed"

os.environ["TESTING"] = "1"
os.environ["REDIS_PORT"] = "26379"
os.environ["POSTGRES_PORT"] = "25432"

import asyncio
import json
from asyncio import AbstractEventLoop
from pathlib import Path
from time import sleep
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.enums import TableNames
from src.core.utils import postgres_dsn
from src.db.postgres.database import get_db
from src.mail import get_send_confirm_link
from src.main import app

from .utils import Docker, Storage, Users, mock_send_confirm_link

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_NAME = os.getenv("POSTGRES_NAME")
REDIS_PORT = os.getenv("REDIS_PORT")

BACKEND_DIR = Path(__file__).parent.parent.resolve()


API_V1_URL = "/api/v1"

AUTH_URL = API_V1_URL + "/auth"
REG_URL = AUTH_URL + "/registration"
CONFIRM_URL = AUTH_URL + "/confirm"
TOKEN_URL = AUTH_URL + "/token"
CHANGE_PASSWORD_URL = AUTH_URL + "/change_password"
FORGET_PASSWORD = AUTH_URL + "/forget_password"

USERS_URL = API_V1_URL + "/users"
ME_URL = USERS_URL + "/me"


postgres_url = postgres_dsn(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
)


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Create a new async loop to test with increase scope to `session`.

    #### Yields:
    - AbstractEventLoop
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def databases_and_migrations() -> Generator[None, None, None]:
    """Create databases for tests andapply migrations.

    #### Yields:
    - None
    """
    docker = Docker(
        redis_port=REDIS_PORT,
        postgres_port=POSTGRES_PORT,
        postgres_user=POSTGRES_USER,
        postgres_password=POSTGRES_PASSWORD,
    )
    docker.run_all()
    sleep(1)
    config = Config("alembic.ini")
    command.upgrade(config, "head")

    yield

    command.downgrade(config, "base")  # not necessary
    docker.stop_all()


@pytest.fixture(scope="session")
async def get_test_sessiom_maker(
    databases_and_migrations,
) -> Generator[sessionmaker, None, None]:
    """Create sessionmaker for getting connections to database.

    #### Args:
    - databases_and_migrations (None):
        Waiting for the database to be created.

    #### Yields:
    - sessionmaker:
        Sessionmaker for getting connections to database.
    """
    test_engine = create_async_engine(
        url=postgres_url,
        future=True,
    )
    TestSession = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    yield TestSession


@pytest.fixture(scope="function", autouse=True)
async def clean_db(get_test_sessiom_maker: sessionmaker) -> None:
    """Clear the database of data

    #### Args:
    - get_test_sessiom_maker (sessionmaker):
        Sessionmaker for getting connections to database.
    """
    async with get_test_sessiom_maker() as session:
        session: AsyncSession
        async with session.begin():
            for table in TableNames:
                await session.execute(
                    text(f"""TRUNCATE TABLE {table} CASCADE;""")
                )


async def get_test_db() -> Generator[AsyncSession, None, None]:
    """Get connection to the test database.

    #### Yields:
    - AsyncSession:
        Connection to the test database.
    """
    test_engine = create_async_engine(
        url=postgres_url,
        future=True,
    )
    TestSession = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with TestSession() as session:
        yield session


@pytest.fixture(name="http_client")
def get_http_client() -> Generator[TestClient, None, None]:
    """HTTP client for testing the application.

    #### Yields:
    - TestClient
    """
    with TestClient(app) as client:
        app.dependency_overrides[get_db] = get_test_db
        app.dependency_overrides[
            get_send_confirm_link
        ] = mock_send_confirm_link

        yield client

        app.dependency_overrides.clear()


@pytest.fixture(name="confirm_link")
def get_reg_confirm_link(http_client: TestClient) -> str:
    """Get a link to confirm registration from the app.

    #### Args:
    - http_client (TestClient):
        HTTP client for testing the application.

    #### Returns:
    - str:
        Confirm_link.
    """
    http_client.post(url=REG_URL, json=Users.user_1)
    return Storage.confirm_link


@pytest.fixture(name="token_user_1")
def get_token_user_1(http_client: TestClient) -> tuple[TestClient, str]:
    """Get the `JWT token` for the logged in test user.

    #### Args:
    - http_client (TestClient):
        HTTP client for testing the application.

    #### Returns:
    - tuple[TestClient, str]:
        HTTP client for reusing and `JWT-token`.
    """
    # registration
    response = http_client.post(url=REG_URL, json=Users.user_1)
    assert response.status_code == 202, response.text
    # confirmation
    response = http_client.get(url=Storage.confirm_link)
    # getting token
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": Users.user_1["email"],
                "password": Users.user_1["password"],
            }
        ),
    )
    token = json.loads(response.text)["access_token"]

    return http_client, token
