from pydantic import Field, validator
from sqlalchemy import Boolean, Column, Integer, String

from src.config import Limits
from src.core.enums import TableNames, UserType
from src.core.mixins.models import EmailTable
from src.core.validators import email_validator
from src.db.postgres.database import Base

from .schemes import CreateTempUserScheme


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


class AuthModel(Base, EmailTable):
    """Table for authentication data.

    #### Attrs:
    - id (int):
        Iidentifier.
    - email (str):
        User's email.
    - is_active (bool): Default False.
        Is the user activated.
    - user_type (int):
        UserType.
    - password (str):
        Hashed pasword.
    """

    __tablename__ = TableNames.AUTH

    is_active = Column(
        Boolean,
        default=False,
    )
    user_type = Column(
        Integer,
        default=UserType.PARENT.value,
        nullable=False,
    )
    password = Column(String(Limits.MAX_LEN_HASH_PASSWORD), nullable=False)
