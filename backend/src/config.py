import os
from pathlib import Path

from email_validator import EMAIL_MAX_LENGTH
from pydantic import BaseSettings, EmailStr, PostgresDsn, SecretStr

BASE_DIR = Path(__file__).parent

MAIL_TEMPLATES_DIR = BASE_DIR / "mail" / "templates"

CONFIRM_REG_HTML = "confirm_reg.html"

MINUTE = 60  # 60 seconds
DAY = MINUTE * 60 * 24


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

    secret_key: str = ",gcf975j@jg"  # salt for hashing password
    algorithm: str = "HS256"  # algorithm for hashing password

    postgres_url: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432"
    )
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_auth_db: int = 1
    redis_cache_db: int = 2

    google_smtp_host: str = "smtp.gmail.com"
    google_smtp_port: int = 465
    google_email: EmailStr = "example@gmail.com"
    google_smtp_password: SecretStr = "app_key"

    admin_email: EmailStr = "admin@admin.qq"
    admin_password: SecretStr = "12345678"

    class Config:
        if os.environ.get("TEST"):
            env_file = ".envdev"
        else:
            env_file = ".env"


class Limits:
    MIN_LEN_USERNAME = 3
    MAX_LEN_USERNAME = 32
    MAX_LEN_HUMAN_NAME = 128
    MIN_LEN_PROVIDER_NAME = 5
    MAX_LEN_PROVIDER_NAME = 256
    MAX_LEN_PROVIDER_DESCRIPTION = 5000
    MAX_LEN_EMAIL = EMAIL_MAX_LENGTH
    MIN_LEN_PASSWORD = 8
    MAX_LEN_PASSWORD = 32
    MAX_LEN_HASH_PASSWORD = 64
    MAX_LEN_HASH_PASSWORD = 128
    MIN_PHONE_NUMBER = 7_900_000_00_00
    MAX_PHONE_NUMBER = 8_000_000_00_00
    DEFAULT_PAGINATION_SIZE = 10
    CONFIRM_EXPIRE_TIME = MINUTE * 13
    TOKEN_EXPIRE_TIME = DAY


settings = AppSettings()
