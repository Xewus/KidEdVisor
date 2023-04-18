import json

import pytest
from fastapi.testclient import TestClient

from ..conftest import API_V1_URL, REG_URL, TOKEN_URL
from ..utils import Storage, Users

PARENTS_URL = API_V1_URL + "/parents"
ME_URL = PARENTS_URL + "/me"

INVALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e"
"yJzdWIiOiJ1c2VyMRBtYWlsLm1haWwiLCJ1dCI6MSwiZXhwIjoxNjc"
"5Mjk4NTkyfQ.KzR7Tv_VHMcBYvnCT8wW1We8Nqw0KbtXhXPgLSJ8VXQ"


@pytest.fixture(name="token_parent_1")
def get_token_parent_1(http_client: TestClient) -> tuple[TestClient, str]:
    """Get the `JWT token` for the logged test parent.

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
