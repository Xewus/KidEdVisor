from time import time

from email_validator import (
    EmailNotValidError,
    EmailUndeliverableError,
    validate_email,
)

from src.config import Limits

from .exceptions import BadRequestException


def email_validator(email: str) -> str:
    """Validate and normalize email address.

    #### Args:
    - email (str):
        Email address for validation.

    #### Raises:
    - BadRequestException:
        Invalid email addres.

    #### Returns:
    - str:
        Valid email addres.
    """
    try:
        email = validate_email(email).email.lower()
    except (EmailNotValidError, EmailUndeliverableError) as exc:
        raise BadRequestException(exc.args)

    return email


def password_validator(password: str) -> str:
    """Check password for complexity.

    #### Args:
    - password (str):
        Password to check.

    #### Raises:
    - ValueError:
        Password is too simple.

    #### Returns:
    - str:
        Checked password.
    """
    if len(set(password)) < len(password) >> 1:
        raise ValueError("password is too simple")

    return password


def is_adult_validator(born: int) -> int:
    """Checking that a person's age is within acceptable limits.

    #### Args:
    - born (int):
        User's date of birth as `1041454800`.

    #### Raises:
    - ValueError:
        Wrong age.

    #### Returns:
    - int:
        Cheked date of birth.
    """
    if born + Limits.ADULT_AGE > time():
        raise ValueError("you are so young")

    if born < time() - Limits.MAX_AGE:
        raise ValueError("you are too old")

    return born
