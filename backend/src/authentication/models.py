"""ORM models.
"""
from typing import TYPE_CHECKING, Optional

from pydantic import validator
from sqlmodel import Field, Relationship

from src.config import Limits
from src.core.mixins import NamedTable, WithIDTable
from src.core.validators import email_validator

from .schemes import CreateTempUserScheme

if TYPE_CHECKING:  # pragma: no cover
    from src.users.models import ParentModel


class TempUserModel(CreateTempUserScheme):
    """Model for temporary storage of user data.

    #### Attrs:
    - email (str):
        User's email.
    - user_type (int):
        UserType.
    - password (str):
        Hashed pasword.
    """

    password: str = Field(
        title="Hashed password",
        max_length=64,
    )

    _good_email = validator("email", allow_reuse=True)(email_validator)


class AuthModel(NamedTable, WithIDTable, TempUserModel, table=True):
    """Table for authentication data.

    #### Attrs:
    - id (int):
        Iidentifier.
    - user_type (int):
        UserType.
    - password (str):
        Hashed pasword.
    - email (str):
        User's email.
    - is_active (bool): Default False.
        Is the user activated.
    """

    email: str = Field(
        unique=True,
        index=True,
        max_length=Limits.MAX_LEN_EMAIL,
    )
    is_active: bool = Field(
        default=False,
        description="Is the user activated",
    )

    # For sqlalchemy, not table field.
    parent: Optional["ParentModel"] = Relationship(back_populates="auth")
