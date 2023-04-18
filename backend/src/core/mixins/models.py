from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.config import Limits


class HumanModel:
    """The mixin for creating user models.

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


class EmailModel:
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


class PhoneNumberModel:
    """Specifies column type as `int8` for Postgres.

    #### Attrs:
    - number (int):
        Big integer (int64) field.
    """

    number: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )
