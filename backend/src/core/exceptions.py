from typing import Any

from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    """Status 400."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "incorrect data"

    def __init__(
        self,
        detail: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if detail is not None:
            self.detail = detail

        super().__init__(self.status_code, self.detail, headers)


class CredentialsException(BadRequestException):
    """Status 401."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "could not validate credentials"


class ForbiddenException(BadRequestException):
    """Status 403."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "access is denied"


class NotFoundException(BadRequestException):
    """Status 404."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "not found"


class UnprocessableEntityException(BadRequestException):
    """Status 422."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = ""


class ServerError(BadRequestException):
    """Status 500."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""
