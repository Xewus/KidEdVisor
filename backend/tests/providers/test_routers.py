import json
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from .conftest import INVALID_TOKEN, ME_URL, MY_INSTITUTIONS


@pytest.mark.smoke
class TestAccessToEndpoints:
    async def test_access_to_me_endpoint(self, http_client: TestClient):
        # no these methods
        assert (
            http_client.post(url=ME_URL).status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )
        assert (
            http_client.put(url=ME_URL).status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

        # no token
        assert (
            http_client.get(url=ME_URL).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.patch(url=ME_URL).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.delete(url=ME_URL).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

        # invalid token
        assert (
            http_client.get(
                url=ME_URL,
                headers={"Authorization": "Bearer " + INVALID_TOKEN},
            ).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.patch(
                url=ME_URL,
                headers={"Authorization": "Bearer " + INVALID_TOKEN},
            ).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.delete(
                url=ME_URL,
                headers={"Authorization": "Bearer " + INVALID_TOKEN},
            ).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

    async def test_access_to_my_institution_endpoint(
        self, http_client: TestClient
    ):
        # no these methods
        assert (
            http_client.put(url=MY_INSTITUTIONS).status_code
            == status.HTTP_405_METHOD_NOT_ALLOWED
        )

        # no token
        assert (
            http_client.get(url=MY_INSTITUTIONS).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.post(url=MY_INSTITUTIONS).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.patch(url=MY_INSTITUTIONS).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.delete(url=MY_INSTITUTIONS).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

        # invalid token
        assert (
            http_client.get(
                url=MY_INSTITUTIONS,
                headers={"Authorization": "Bearer " + INVALID_TOKEN},
            ).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.post(
                url=MY_INSTITUTIONS,
                headers={"Authorization": "Bearer " + INVALID_TOKEN},
            ).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.patch(
                url=MY_INSTITUTIONS,
                headers={"Authorization": "Bearer " + INVALID_TOKEN},
            ).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        assert (
            http_client.delete(
                url=MY_INSTITUTIONS,
                headers={"Authorization": "Bearer " + INVALID_TOKEN},
            ).status_code
            == status.HTTP_401_UNAUTHORIZED
        )


@pytest.mark.usefixtures("clean_db")
class TestSelfManageOwner:
    def test_get_me(self, token_owner_1: tuple[TestClient, str]):
        http_client, token = token_owner_1

        response = http_client.get(
            url=ME_URL,
            headers={"Authorization": "Bearer " + token},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        assert set(json.loads(response.text).keys()).issubset(
            {"name", "surname", "patronic", "born"}
        )

    def test_delete_me(self, token_owner_1: tuple[TestClient, str]):
        http_client, token = token_owner_1

        # me exist
        response = http_client.get(
            url=ME_URL,
            headers={"Authorization": "Bearer " + token},
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        # delete me
        response = http_client.delete(
            url=ME_URL,
            headers={"Authorization": "Bearer " + token},
        )
        assert (
            response.status_code == status.HTTP_204_NO_CONTENT
        ), response.text

        # me not exist
        response = http_client.get(
            url=ME_URL,
            headers={"Authorization": "Bearer " + token},
        )
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
        ), response.text

    @pytest.mark.parametrize(
        "update_data, status_code, expect_data",
        [
            # 0 empty data
            (
                {},
                status.HTTP_200_OK,
                {
                    "name": None,
                    "surname": None,
                    "patronic": None,
                    "born": None,
                },
            ),
            # 1 only name
            (
                {
                    "name": "john",
                },
                status.HTTP_200_OK,
                {
                    "name": "John",
                    "surname": None,
                    "patronic": None,
                    "born": None,
                },
            ),
            # 2 only surname
            (
                {
                    "name": None,
                    "surname": "doE",
                },
                status.HTTP_200_OK,
                {
                    "name": None,
                    "surname": "Doe",
                    "patronic": None,
                    "born": None,
                },
            ),
            # 3 only patronic
            (
                {
                    "patronic": "Ibn aBu DAkar",
                },
                status.HTTP_200_OK,
                {
                    "name": None,
                    "surname": None,
                    "patronic": "Ibn Abu Dakar",
                    "born": None,
                },
            ),
            # 4 only born
            (
                {
                    "name": None,
                    "surname": None,
                    "born": 1041454800,
                },
                status.HTTP_200_OK,
                {
                    "name": None,
                    "surname": None,
                    "patronic": None,
                    "born": 1041454800,
                },
            ),
            # 5 full update
            (
                {
                    "name": "John",
                    "surname": "Doe",
                    "patronic": "Ibn Abu Dakar",
                    "born": 1041454800,
                },
                status.HTTP_200_OK,
                {
                    "name": "John",
                    "surname": "Doe",
                    "patronic": "Ibn Abu Dakar",
                    "born": 1041454800,
                },
            ),
            # 6 too young
            (
                {
                    "born": 1672606800,
                },
                status.HTTP_400_BAD_REQUEST,
                {},
            ),
            # 7 too old
            (
                {
                    "born": -2208911417,
                },
                status.HTTP_400_BAD_REQUEST,
                {},
            ),
        ],
    )
    def test_update_me(
        self,
        token_owner_1: tuple[TestClient, str],
        update_data: dict[str, Any],
        status_code: int,
        expect_data: dict[str, Any],
    ):
        http_client, token = token_owner_1

        response = http_client.get(
            url=ME_URL,
            headers={"Authorization": "Bearer " + token},
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        # before update parent must is clean
        me = json.loads(response.text)
        assert me["name"] is None
        assert me["surname"] is None
        assert me["patronic"] is None
        assert me["born"] is None

        # request with update data
        response = http_client.patch(
            url=ME_URL,
            json=update_data,
            headers={"Authorization": "Bearer " + token},
        )
        assert response.status_code == status_code, response.text

        # get updated parent
        response = http_client.get(
            url=ME_URL,
            headers={"Authorization": "Bearer " + token},
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        me: dict = json.loads(response.text)

        if status_code == status.HTTP_200_OK:
            assert me == expect_data


@pytest.mark.usefixtures("clean_db")
class TestSelfManageInstitution:
    def test_get_my_no_institutions(
        self, token_owner_1: tuple[TestClient, str]
    ):
        http_client, token = token_owner_1
        # me exist
        response = http_client.get(
            url=ME_URL,
            headers={"Authorization": "Bearer " + token},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response = http_client.get(
            url=MY_INSTITUTIONS,
            headers={"Authorization": "Bearer " + token},
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        # no institutions
        data = json.loads(response.text)
        assert data == []
