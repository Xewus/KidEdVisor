import json

import pytest
from fastapi.testclient import TestClient

from ..conftest import REG_URL, TOKEN_URL
from ..utils import Storage, Users


@pytest.fixture(name="confirm_link")
def get_reg_confirm_link(http_client: TestClient) -> str:
    """Get a link to confirm registration from the app for user.

    #### Args:
    - http_client (TestClient):
        HTTP client for testing the application.

    #### Returns:
    - str:
        Confirm_link.
    """
    http_client.post(url=REG_URL, json=Users.parent_1)
    return Storage.confirm_link


@pytest.fixture(name="token_user_1")
def get_token_user_1(http_client: TestClient) -> tuple[TestClient, str]:
    """Get the `JWT token` for the logged test user.

    #### Args:
    - http_client (TestClient):
        HTTP client for testing the application.

    #### Returns:
    - tuple[TestClient, str]:
        HTTP client for reusing and `JWT-token`.
    """
    # registration
    response = http_client.post(url=REG_URL, json=Users.parent_1)
    assert response.status_code == 202, response.text
    # confirmation
    response = http_client.get(url=Storage.confirm_link)
    assert response.status_code == 200, response.text
    # getting token
    response = http_client.post(
        url=TOKEN_URL,
        data=(
            {
                "username": Users.parent_1["email"],
                "password": Users.parent_1["password"],
            }
        ),
    )
    assert response.status_code == 200, response.text
    token = json.loads(response.text)["access_token"]

    return http_client, token
