import json
import os
import sys
from pprint import pprint

assert (sys.version_info.major, sys.version_info.minor) == (
    3,
    11,
), "Only Python 3.11 allowed"

os.environ["TEST"] = "True"

from typing import Callable

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.postgres.database import get_db
from src.mail import get_send_confirm_link
from src.main import app

pprint(dict(os.environ))


API_V1_URL = "/api/v1"

AUTH_URL = API_V1_URL + "/auth"
REG_URL = AUTH_URL + "/registration"
CONFIRM_URL = AUTH_URL + "/confirm"
TOKEN_URL = AUTH_URL + "/token"
CHANGE_PASSWORD_URL = AUTH_URL + "/change_password"
FORGET_PASSWORD = AUTH_URL + "/forget_password"

USERS_URL = API_V1_URL + "/users"
ME_URL = USERS_URL + "/me"


class Storage:
    confirm_link = "No link"


class Users:
    user_1 = {
        "email": "user1@mail.ru",
        "password": "password1",
    }
    user_2 = {
        "email": "user2@mail.ru",
        "password": "password2",
        "user_type": 1,
    }
    teacher_1 = {
        "email": "teacher1@gmail.com",
        "password": "password1",
        "user_type": 2,
    }
    teacher_2 = {
        "email": "teacher2@gmail.com",
        "password": "password2",
        "user_type": 2,
    }
    institution_1 = {
        "email": "institution1@yahoo.com",
        "password": "password1",
        "user_type": 3,
    }
    institution_2 = {
        "email": "institution2@yahoo.com",
        "password": "password2",
        "user_type": 3,
    }


test_engine = create_async_engine(
    # "sqlite+aiosqlite:///./test.db",
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    future=True,
)

TestSession = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


@pytest_asyncio.fixture(scope="function")
async def init_test_db() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_test_db() -> AsyncSession:
    async with TestSession() as session:
        yield session


def send_confirm_link_for_tests() -> Callable:
    def save_confirm_link(email: str, confirm_link: str) -> None:
        Storage.confirm_link = confirm_link

    return save_confirm_link


@pytest.fixture(name="http_client")
def get_http_client(init_test_db) -> TestClient:
    with TestClient(app) as client:
        app.dependency_overrides[get_db] = get_test_db
        app.dependency_overrides[
            get_send_confirm_link
        ] = send_confirm_link_for_tests

        yield client

        app.dependency_overrides.clear()


@pytest.fixture(name="confirm_link")
def get_comfirm_link(http_client: TestClient) -> str:
    http_client.post(url=REG_URL, json=Users.user_1)
    return Storage.confirm_link


@pytest.fixture(name="token_user_1")
def get_token_user_1(http_client: TestClient) -> tuple[TestClient, str]:
    # registration
    http_client.post(url=REG_URL, json=Users.user_1)
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
