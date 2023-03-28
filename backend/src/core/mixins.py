import re
from datetime import date

from pydantic import EmailStr, Field, validator
from sqlalchemy.orm import declared_attr
from sqlmodel import BigInteger, Column
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel

from src.config import Limits

from .enums import UserType
from .validators import password_validator


class NamedTable(SQLModel):
    """Mixin to standardize table names.
    The class name should end with `Model`.

    #### Examples:
    - `UserModel` -> `user`
    - `ParentChildModel` -> `parent_child`
    """

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__.rstrip("Model")
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        return name


class WithIDTable(SQLModel):
    """Mixin to add `id` field to table with integer type as primary key.

    #### Attrs:
    - id (int | None):
        Primary key for table.
    """

    id: int | None = SQLField(default=None, primary_key=True)


class UserTypeScheme(SQLModel):
    """Scheme for user type.

    #### Attrs:
    - user_type (int): Default `1`.
        UserType.
    """

    user_type: int | None = Field(
        default=UserType.PARENT.value,
        description="There are 3 params: user`1`, tutor`2`, institution`3`",
    )


class HumanScheme(SQLModel):
    """The base schema for creating user schemas.

    #### Attrs:
    - name: (str | None):
        Real user's name.
    - surname: (str | None):
        Real user's last name.
    - patronic: (str | None):
        Real user's patronic name.
    - born: (date | None):
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
    born: date | None = Field(
        default=None,
        title="User's date of birth",
    )


class EmailScheme(SQLModel):
    """The base schema for creating email contact schemas.

    #### Attrs:
    - email (str):
        User's email.
    """

    email: EmailStr = Field(
        title="User's email",
        example="example@gmail.com",
    )


class PasswordScheme(SQLModel):
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
class PhoneScheme(SQLModel):
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


class PhoneNumberPgDB(SQLModel):
    """Specifies column type as `int8` for Postgres.

    #### Attrs:
    - phone_number (int):
        Big integer (int64) field.
    """

    phone_number: int | None = Field(
        default=None,
        sa_column=Column(BigInteger),
    )
