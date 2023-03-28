from pydantic import Field, validator

from src.config import Limits
from src.core.mixins import HumanScheme
from src.core.validators import is_adult_validator


class BaseParentScheme(HumanScheme):
    """The base schema for parent schemas.

    #### Attrs:
    - name: (str | None):
        Real parent's name.
    - surname: (str | None):
        Real parent's last name.
    - patronic: (str | None):
        Real parent's patronic name.
    - born: (date | None):
        Parent's date of birth as UNIX time.
    """


class CreateParentScheme(BaseParentScheme):
    """Scheme for parent creation.

    #### Attrs:
    - name: (str | None):
        Real parent's name.
    - surname: (str | None):
        Real parent's last name.
    - patronic: (str | None):
        Real parent's patronic name.
    - born: (date | None):
        Parent's date of birth as UNIX time.
    """

    _adult_born = validator("born", allow_reuse=True)(is_adult_validator)

    @validator("name", "surname", "patronic")
    def names_validator(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.title()


class ResponseParentScheme(BaseParentScheme):
    """Scheme for data of parent for issuing to the outside.

    #### Attrs:
    - name: (str | None):
        Real parent's name.
    - surname: (str | None):
        Real parent's last name.
    - patronic: (str | None):
        Real parent's patronic name.
    - born: (date | None):
        Parent's date of birth as UNIX time.
    - email (str | None):
        Parent's email.
    """


class ResponseParentAuthScheme(BaseParentScheme):
    """Scheme for data of parent for issuing to the outside.

    #### Attrs:
    - name: (str | None):
        Real parent's name.
    - surname: (str | None):
        Real parent's last name.
    - patronic: (str | None):
        Real parent's patronic name.
    - born: (date | None):
        Parent's date of birth as UNIX time.
    - email (str):
        Parent's email.
    """

    email: str = Field(
        max_length=Limits.MAX_LEN_EMAIL,
    )


class UpdateParentScheme(CreateParentScheme):
    """Scheme for updating parent data."""
