from pydantic import BaseModel, Field, validator

from src.core.enums import UserType
from src.core.mixins import EmailScheme, PasswordScheme, UserTypeScheme


class BaseAuthScheme(EmailScheme, UserTypeScheme):
    """Base scheme for authntication.

    #### Attrs:
    - email (str):
        User's email.
    - user_type (int): Default `1`.
        UserType.
    """


class CreateTempUserScheme(BaseAuthScheme, PasswordScheme):
    """Scheme for first registration.

    #### Attrs:
    - email (str):
        User's email.
    - user_type (int): Default `1`.
        UserType.
    - password (str):
        Password for authorization.
    """

    @validator("user_type")
    def user_type_validator(cls, user_type: int) -> int:
        if user_type is not None and (
            user_type not in UserType.__members__.values()
            or user_type == UserType.ADMIN
        ):
            raise ValueError("This user type does not exist")

        return user_type


class TokenScheme(BaseModel):
    """Scheme for `Bearer Token`.

    #### Attrs:
    - access_token (str):
        JWT token.
    - token_type (str): Default `bearer`. Immutable.
    """

    access_token: str = Field(
        description="JWT token",
    )
    token_type: str = Field(
        default="bearer",
    )


class TokenDataScheme(BaseAuthScheme):
    """Schema for the 'JWT' token fields.

    #### Attrs:
    - email (str):
        User's email.
    - user_type (int):
        UserType.
    """
