from pydantic import Field, validator
from src.config import Limits
from src.core.mixins import HumanScheme
from src.core.validators import is_adult_validator


class BaseOwnerScheme(HumanScheme):
    """The base schema for owner schemas.

    #### Attrs:
    - name (str | None):
        Real owner's name.
    - surname (str | None):
        Real owner's last name.
    - patronic (str | None):
        Real owner's patronic name.
    - born (int | None):
        Parent's date of birth as UNIX time.
    """


class CreateOwnerScheme(BaseOwnerScheme):
    """Scheme for owner creation.

    #### Attrs:
    - name (str):
        Real owner's name.
    - surname (str):
        Real owner's last name.
    - patronic (str | None):
        Real owner's patronic name.
    - born (int):
        owner's date of birth as UNIX time.
    """

    name: str = Field(
        title="Real user's name",
        example="John",
        max_length=Limits.MAX_LEN_HUMAN_NAME,
    )
    surname: str = Field(
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
    born: int = Field(
        title="User's date of birth",
        description="Date fotmat as `unixtime`",
        example=1041454800,
    )

    _adult_born = validator("born", allow_reuse=True)(is_adult_validator)

    @validator("name", "surname", "patronic")
    def names_validator(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.title()


class UpdateOwnerScheme(BaseOwnerScheme):
    """Scheme for updating owner data.

    #### Attrs:
    - name (str | None):
        Real owner's name.
    - surname: (str | None):
        Real owner's last name.
    - patronic (str | None):
        Real owner's patronic name.
    - born (int | None):
        Parent's date of birth as UNIX time.
    """

    _adult_born = validator("born", allow_reuse=True)(is_adult_validator)

    @validator("name", "surname", "patronic")
    def names_validator(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.title()


class ResponseOwnerScheme(BaseOwnerScheme):
    """Scheme for data of owner for issuing to the outside.

    #### Attrs:
    - name (str):
        Real owner's name.
    - surname (str):
        Real owner's last name.
    - patronic (str | None):
        Real owner's patronic name.
    - born (int):
        Parent's date of birth as UNIX time.
    """

    class Config:
        orm_mode = True
