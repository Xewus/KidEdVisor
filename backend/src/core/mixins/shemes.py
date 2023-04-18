from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from src.config import Limits
from src.core.enums import UserType
from src.core.validators import password_validator


class ShortHttpUrl(HttpUrl):
    max_length = Limits.MAX_LEN_HTTP_URL


class UserTypeScheme(BaseModel):
    """Scheme for user type.

    #### Attrs:
    - user_type (int): Default `1`.
        Type of user.
    """

    user_type: int | None = Field(
        default=UserType.PARENT.value,
        title="User's type",
        description="There are 2 params: user:`1`, owner:`2`",
    )


class HumanScheme(BaseModel):
    """The base schema for creating user schemas.

    #### Attrs:
    - name (str | None):
        Real user's name.
    - surname (str | None):
        Real user's last name.
    - patronic (str | None):
        Real user's patronic name.
    - born (int | None):
        User's date of birth as UNIX time.
    """

    name: str | None = Field(
        default=None,
        title="Real user's name",
        example="John",
        max_length=Limits.MAX_LEN_HUMAN_NAME,
    )
    surname: str | None = Field(
        default=None,
        title="Real user's last name",
        example="Doe",
        max_length=Limits.MAX_LEN_HUMAN_NAME,
    )
    patronic: str | None = Field(
        default=None,
        title="Real user's patronic name",
        example="Ibn Abu Dakar",
        max_length=Limits.MAX_LEN_HUMAN_NAME,
    )
    born: int | None = Field(
        default=None,
        title="User's date of birth",
        description="Date fotmat as `unixtime`",
        example=1041454800,
    )


class EmailScheme(BaseModel):
    """The base schema for creating email contact schemas.

    #### Attrs:
    - email (str):
        User's email.
    """

    email: EmailStr = Field(
        title="User's email",
        example="example@gmail.com",
    )


class PasswordScheme(BaseModel):
    """The base schema for creating password schemas.

    #### Attrs:
    - password (str):
        Password for authorization.
    """

    password: str = Field(
        title="Password for authorization",
        example="qwe7RTY8asd",
        min_length=Limits.MIN_LEN_PASSWORD,
        max_length=Limits.MAX_LEN_PASSWORD,
    )

    _good_password = validator("password", allow_reuse=True)(
        password_validator
    )


# for future
class PhoneScheme(BaseModel):
    """The base schema for creating phone contact schemas.

    #### Attrs:
    - phone_number (int | None):
        Contact phone number.
    """

    phone_number: int | None = Field(
        default=None,
        title="Contact phone number",
        example=79012223344,
        gt=Limits.MIN_PHONE_NUMBER,
        lt=Limits.MAX_PHONE_NUMBER,
    )
