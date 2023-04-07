from enum import IntEnum, StrEnum

from src.config import settings


class TableNames(StrEnum):
    """
    #### Attrs:
    AUTH (str): "auth"
    PARENT (str): "parent"
    OWNER (str): "owner"
    INSTITUTION (str): "nstitution"
    TEACHER (str): "teacher"
    """

    AUTH = "auth"
    PARENT = "parent"
    OWNER = "owner"
    INSTITUTION = "institution"
    TEACHER = "teacher"


class UserType(IntEnum):
    """
    #### Attrs:
    - PARENT (int): 1
    - OWNER (int): 2
    - ADMIN (int): 42
    """

    PARENT = 1
    OWNER = 2
    ADMIN = 42


class InstitutionType(IntEnum):
    """
    #### Attrs:
    - KINDERGARTEN (int): 100
    - SCHOOL (int): 200
    - HIGH_SCHOOL (int): 201
    - PRIVATE_SCHOOL (int): 202
    - COLLEGE (int): 300
    - INSTITUTE (int): 400
    - UNIVERSITY (int): 401
    - ADDITIONAL (int): 500
    - SPORT (int): 600
    - CREATION (int): 700
    - SCIENCE (INT): 800
    """

    KINDERGARTEN = 100
    SCHOOL = 200
    HIGH_SCHOOL = 201
    PRIVATE_SCHOOL = 202
    COLLEGE = 300
    INSTITUTE = 400
    UNIVERSITY = 401
    ADDITIONAL = 500
    SPORT = 600
    CREATION = 700
    SCIENCE = 800


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
