from datetime import date, timedelta

from email_validator import (
    EmailNotValidError,
    EmailUndeliverableError,
    validate_email,
)

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


def is_adult_validator(born: date) -> date:
    """Checking that a person's age is within acceptable limits.

    #### Args:
    - born (date):
        User's date of birth as `1987-01-23`.

    #### Raises:
    - ValueError:
        Wrong age.

    #### Returns:
    - date:
        Cheked date of birth.
    """
    today = date.today()
    min_age = today - timedelta(days=365 * 18 + 5)
    if born > min_age:
        raise ValueError("you are so young")

    max_age = today - timedelta(days=365 * 99)
    if born < max_age:
        raise ValueError("you are too old")

    return born
