from enum import IntEnum, StrEnum

from src.config import settings


class UserType(IntEnum):
    """
    #### Attrs:
    - PARENT (int): 1
    - TEACHER (int): 2
    - INSTITUTION (int): 3
    - ADMIN (int): 42
    """

    PARENT = 1
    TEACHER = 2
    INSTITUTION = 3
    ADMIN = 42


class AppPaths(StrEnum):
    """
    #### Attrs:
    - AUTHENTICATION (str): "/auth"
    - USERS (str): "/users"
    - PROVIDERS (str): "/providers"
    """

    AUTHENTICATION = "/auth"
    USERS = "/users"
    PROVIDERS = "/providers"


class RouteTags(StrEnum):
    """Tags for routes.

    #### Attrs:
    - ADMIN (str): "ADMIN"
    - AUTH (str): "AUTH"
    - USERS (str): "USERS"
    - PROVIDERS (str): "PROVIDERS"
    - PROFILE (str): "PROFILE"
    """

    ADMIN = "ADMIN"
    AUTH = "AUTH"
    USERS = "USERS"
    PROVIDERS = "PROVIDERS"
    PROFILE = "PROFILE"


class SendEmailFrom(StrEnum):
    """
    #### Attrs:
    - GOOGLE (str): from settings
    """

    GOOGLE = settings.google_email
