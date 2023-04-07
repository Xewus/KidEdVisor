import os
from pathlib import Path

from dotenv import load_dotenv
from email_validator import EMAIL_MAX_LENGTH
from pydantic import BaseSettings, EmailStr, SecretStr

load_dotenv()

BACKEND_DIR = Path(__file__).parent.parent.resolve()

MAIL_TEMPLATES_DIR = BACKEND_DIR / "src/mail/templates"

CONFIRM_REG_HTML = "confirm_reg.html"

MINUTE = 60  # 60 seconds
DAY = MINUTE * 60 * 24
YEAR = DAY * 365


class RedisPrefixes:
    TEMP_USER = "tempuser:"
    NEWPASSWORD = "newpassword:"


class AppSettings(BaseSettings):
    """Get settings from `.env` file.

    Use uppercase for the names of the values in the file.
    """

    debug: bool = False
    path: str  # ENV PATH from os
    app_title: str = "Template"
    app_version: str = "0.0.0"
    app_description: str = "FastAPI app"
    api_v1_prefix: str = "/api/v1"

    secret_key: str  # salt for hashing password
    algorithm: str  # algorithm for hashing password

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db_name: str

    redis_host: str
    redis_port: int
    redis_auth_db: int
    redis_cache_db: int

    google_smtp_host: str = "smtp.gmail.com"
    google_smtp_port: int = 465
    google_email: EmailStr = "example@gmail.com"
    google_smtp_password: SecretStr = "app_key"

    admin_email: EmailStr = "admin@admin.qq"
    admin_password: SecretStr = "12345678"

    class Config:
        if os.getenv("TESTING"):
            env_file = ".envdev"
        else:
            env_file = ".env"


class Limits:
    ADULT_AGE = 18 * YEAR + 5 * DAY
    MAX_AGE = 100 * YEAR

    MIN_LEN_USERNAME = 3
    MAX_LEN_USERNAME = 32
    MAX_LEN_HUMAN_NAME = 128

    MIN_LEN_PROVIDER_NAME = 5
    MAX_LEN_PROVIDER_NAME = 256

    MIN_LEN_PASSWORD = 8
    MAX_LEN_PASSWORD = 32

    MIN_PHONE_NUMBER = 7_900_000_00_00
    MAX_PHONE_NUMBER = 8_000_000_00_00

    MAX_LEN_PROVIDER_DESCRIPTION = 512
    MAX_LEN_EMAIL = EMAIL_MAX_LENGTH  # from pydantic
    MAX_LEN_HASH_PASSWORD = 128

    CONFIRM_EXPIRE_TIME = MINUTE * 13
    TOKEN_EXPIRE_TIME = DAY

    DEFAULT_PAGINATION_SIZE = 10


settings = AppSettings()
