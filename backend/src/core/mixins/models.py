from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config import Limits


class HumanTable:
    """The mixin for creating user models.

    #### Attrs:
    - name: (str | None):
        Real user's name.
    - surname: (str | None):
        Real user's last name.
    - patronic: (str | None):
        Real user's patronic name.
    - born: (int | None):
        User's date of birth as UNIX time.
    """

    name: Mapped[str | None] = mapped_column(
        String(Limits.MAX_LEN_HUMAN_NAME),
        default=None,
    )
    surname: Mapped[str | None] = mapped_column(
        String(Limits.MAX_LEN_HUMAN_NAME),
        default=None,
    )
    patronic: Mapped[str | None] = mapped_column(
        String(Limits.MAX_LEN_HUMAN_NAME),
        default=None,
    )
    born: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
    )


class EmailTable:
    """The mixin for creating email contact models.

    #### Attrs:
    - email (str):
        User's email.
    """

    email: Mapped[str] = mapped_column(
        String(Limits.MAX_LEN_EMAIL),
        unique=True,
        index=True,
        nullable=False,
    )


class PhoneNumberTable:
    """Specifies column type as `int8` for Postgres.

    #### Attrs:
    - phone_number (int):
        Big integer (int64) field.
    """

    phone_number: Mapped[int] = mapped_column(
        BigInteger,
        default=None,
    )
