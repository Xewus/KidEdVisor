import json
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.conftest import (
    CHANGE_PASSWORD_URL,
    CONFIRM_URL,
    FORGET_PASSWORD,
    REG_URL,
    TOKEN_URL,
    Storage,
    Users,
)


@pytest.mark.smoke
@pytest.mark.parametrize(
    # [GET, POST, PUT, PATCH, DELETE]
    # (False, False, False, False, False)
    "url, alloweds",
    [
        (REG_URL, (False, True, False, False, False)),
        (CONFIRM_URL + "/" + "a" * 32, (True, False, False, False, False)),
        (TOKEN_URL, (False, True, False, False, False)),
        (CHANGE_PASSWORD_URL, (False, True, False, False, False)),
        (FORGET_PASSWORD, (False, True, False, False, False)),
        (
            FORGET_PASSWORD + "/" + "a" * 32,
            (True, False, False, False, False),
        ),
    ],
)
def test_access_to_endpoint(
    http_client: TestClient, url: str, alloweds: list[bool]
):
    methods = (
        http_client.get,
        http_client.post,
        http_client.put,
        http_client.patch,
        http_client.delete,
    )
    assert len(methods) == len(alloweds)

    for i, allowed in enumerate(alloweds):
        if allowed:
            continue
        assert (
            methods[i](url=url).status_code
            != status.HTTP_405_METHOD_NOT_ALLOWED
        ) is allowed


@pytest.mark.registration
@pytest.mark.parametrize(
    "user, status_code",
    [
        # 0-user
        (
            Users.user_1,
            status.HTTP_202_ACCEPTED,
        ),
        # 1-teacher
        (
            Users.teacher_1,
            status.HTTP_202_ACCEPTED,
        ),
        # 2-institution
        (
            Users.institution_1,
            status.HTTP_202_ACCEPTED,
        ),
        # 3-extra feild
        (
            {
                "email": "user3@yandex.kz",
                "password": "password3",
                "extra": "1234",
            },
            status.HTTP_202_ACCEPTED,
        ),
        # 4-no email
        (
            {
                "password": "password3",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 5-empty email
        (
            {
                "email": "",
                "password": "password3",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 6-bad email
        (
            {
                "email": "user6mail@mail",
                "password": "password3",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 7-no password
        (
            {
                "email": "user7@yndex.kz",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 8-empty password
        (
            {
                "email": "user8@mail.mail",
                "password": "",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 9-simple password
        (
            {
                "email": "user9@mail.mail",
                "password": "qqqqwwwww",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 10-too shirt password
        (
            {
                "email": "user10@mail.mail",
                "password": "1qWe5",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 11-too long password
        (
            {
                "email": "user11@mail.mail",
                "password": "1qWe5" * 9,
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 12-not exists user_type
        (
            {
                "email": "user12@mail.mail",
                "password": "1qWe5DRDht",
                "user_type": 10,
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        # 13-no admin registration
        (
            {
                "email": "user13@mail.mail",
                "password": "1qWe5DRDht",
                "user_type": 42,
            },
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_pre_registration(
    http_client: TestClient,
    user: dict[str, Any],
    status_code: int,
):
    response = http_client.post(url=REG_URL, json=user)
    assert response.status_code == status_code, response.text


@pytest.mark.registration
def test_confirmation(http_client: TestClient, confirm_link: str):
    # t00 short confirm link
    response = http_client.get(url=confirm_link[:-1])
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # too long confirm link
    response = http_client.get(url=confirm_link + "q")
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # non-existent confirm link
    response = http_client.get(url=confirm_link[-1] + "q")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

    # confirm link ok
    response = http_client.get(url=confirm_link)
    assert response.status_code == status.HTTP_200_OK, response.text

    # confirm llink has already been used
    response = http_client.get(url=confirm_link)
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


@pytest.mark.registration
def test_reistration_with_repeat_email(
    http_client: TestClient, confirm_link: str
):
    # confirm link ok
    response = http_client.get(url=confirm_link)
    assert response.status_code == status.HTTP_200_OK, response.text
    # repeat email
    response = http_client.post(url=REG_URL, json=Users.user_1)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), response.text

    # repeat upper email
    user = Users.user_1.copy()
    user["email"] = user["email"].upper()
    response = http_client.post(url=REG_URL, json=Users.user_1)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), response.text

    # repeat email with spaces
    user = Users.user_1.copy()
    user["email"] = " " + user["email"].upper() + "  "
    response = http_client.post(url=REG_URL, json=Users.user_1)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), response.text


@pytest.mark.token
@pytest.mark.password
def test_recive_token(http_client: TestClient, confirm_link: str):
    # create user
    response = http_client.get(url=confirm_link)
    assert response.status_code == status.HTTP_200_OK, response.text

    # without data
    response = http_client.post(url=TOKEN_URL)
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # without email
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "password": Users.user_1["password"],
            }
        ),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # without password
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": "q" + Users.user_1["email"],
            }
        ),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # non-exist emal
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": "q" + Users.user_1["email"],
                "password": Users.user_1["password"],
            }
        ),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # invalid password
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": Users.user_1["email"],
                "password": Users.user_1["password"] + "q",
            }
        ),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # data ok
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": Users.user_1["email"],
                "password": Users.user_1["password"],
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    data = json.loads(response.text)
    assert data["access_token"]


@pytest.mark.token
@pytest.mark.password
def test_password_change(token_user_1: tuple[TestClient, str]):
    http_client, token = token_user_1
    NEW_PASSWORD = "newPassword"

    response = http_client.post(
        url=CHANGE_PASSWORD_URL,
        headers={"Authorization": "Bearer " + token},
        data={"password": NEW_PASSWORD},
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    # get token with new password
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": Users.user_1["email"],
                "password": NEW_PASSWORD,
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    # no token with old password
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": Users.user_1["email"],
                "password": Users.user_1["password"],
            }
        ),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


@pytest.mark.password
def test_forget_password(
    http_client: TestClient, token_user_1: tuple[TestClient, str]
):
    # bad email
    response = http_client.post(
        url=FORGET_PASSWORD, data={"email": "bad@mailru"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # not exists email
    response = http_client.post(
        url=FORGET_PASSWORD, data={"email": "noExistEmail@dmail.com"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    # exists user
    response = http_client.post(
        url=FORGET_PASSWORD, data={"email": Users.user_1["email"]}
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    response = http_client.get(url=Storage.confirm_link)
    assert response.status_code == status.HTTP_200_OK, response.text

    data = json.loads(response.text)
    assert data["password"], "No password in response"
