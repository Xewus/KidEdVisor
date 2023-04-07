from random import SystemRandom
from string import ascii_letters

from pydantic import PostgresDsn

random_choice = SystemRandom().choice


def change_openapi_schema(openapi_schema: dict) -> dict:
    """Change error description in standart OpenAPI schema.

    #### Args:
    - openapi_schema (dict):
        Default OpenAPI schema.

    #### Returns:
    - dict:
        Changed OpenAPI schema.
    """
    new_error_response = {
        "description": "Error",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {"detail": {"type": "string"}},
                }
            }
        },
    }

    paths: dict[str, dict[str, dict]] = openapi_schema["paths"]
    for methods in paths.values():
        for method in methods:
            responses: dict = methods[method]["responses"]
            if responses.get("422") is None:
                continue

            responses["400"] = new_error_response
            responses["422"] = new_error_response
    return openapi_schema


def postgres_dsn(
    user: str,
    password: str,
    host: str,
    port: int,
    db_name: str | None = None,
) -> PostgresDsn:
    dsn = f"postgresql+asyncpg://{user}:{password}@{host}:{port}"
    if db_name:
        dsn = f"{dsn}/{db_name}"
    return dsn


def random_string(length: int) -> str:
    """Create a string with random letters.

    #### Args:
    - length (int):
        Generated string length.

    #### Returns:
    - str:
        Generated string length.
    """
    return "".join(random_choice(ascii_letters) for i in range(length))
