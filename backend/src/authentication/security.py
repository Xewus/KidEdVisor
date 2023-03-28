from time import time

import asyncpg
from asyncpg.connection import Connection
from asyncpg.exceptions import DataError, UniqueViolationError
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Limits, settings
from src.core.enums import AppPaths, UserType
from src.core.exceptions import (
    BadRequestException,
    CredentialsException,
    ForbiddenException,
    NoAdminException,
)
from src.db.postgres.database import get_db

from .crud import auth_crud
from .models import AuthModel
from .schemes import TokenDataScheme

token_url = f"{settings.api_v1_prefix}{AppPaths.AUTHENTICATION}/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> AuthModel | None:
    """Get the active user from the database if the password matches.

    #### Args:
    - db (AsyncSession):
        Connecting to the database.
    - email (str):
        Unique email as an identifier.
    - password (str):
        Password.

    #### Raises:
    - BadRequestException:
        Bad authentication data.

    #### Returns:
    - AuthModel | None:
        The user object from the database if the password matches else None.
    """
    user: AuthModel = await auth_crud.get(db, AuthModel.email == email)
    if user is None or not user.is_active:
        raise BadRequestException(f"user with email: {email} not found")

    if not pwd_context.verify(password, user.password):
        raise BadRequestException("invlid password")

    return user


def create_JWT_token(claims: dict) -> str:
    """Create `JWT` token.

    #### Args:
    - claims (dict):
        Data to encode into a token.

    #### Returns:
    - str:
        Encoded `JWT` token.
    """
    claims["exp"] = Limits.TOKEN_EXPIRE_TIME + int(time())
    token = jwt.encode(claims, settings.secret_key, settings.algorithm)
    return token


def get_token_data(
    token: str = Depends(oauth2_scheme),
) -> TokenDataScheme:
    """Get data from `JWT` token.

    #### Args:
    - token (str):
        JWT token.

    #### Raises:
    - CredentialsException:
        Bad token.

    #### Returns:
    - TokenDataScheme:
        Data from token.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, (settings.algorithm,))
        email = payload.get("sub")
        user_type = payload.get("ut")
        if (email or user_type) is None:
            raise CredentialsException
        token_data = TokenDataScheme(email=email, user_type=user_type)
    except JWTError:
        raise CredentialsException

    return token_data


async def get_token_user(
    db: AsyncSession = Depends(get_db),
    token_data: TokenDataScheme = Depends(get_token_data),
) -> AuthModel:
    """Get a user by `JWT` token.

    #### Args:
    - db (AsyncSession):
        Connecting to the database.
    - token_data (TokenDataScheme):
        Data from JWT token.

    #### Raises:
    - CredentialsException:
        The token is invalid.

    #### Returns:
    - AuthModel:
        The user object from the database.
    """
    user: AuthModel = await auth_crud.get(
        db, AuthModel.email == token_data.email
    )
    if user is None or not user.is_active:
        raise CredentialsException

    return user


async def get_admin_user(
    user: AuthModel = Depends(get_token_user),
) -> AuthModel:
    """Get the user if it is not deactivated and is admin.

    #### Args:
    - user (AuthModel):
        The user object from the database.

    #### Raises:
    - NotActiveUserException:
        The user is not admin.

    #### Returns:
    - AuthModel:
        The user object from the database.
    """
    if user.user_type != UserType.ADMIN:
        raise ForbiddenException

    return user


def get_hash_password(password: str) -> str:
    """Get a hash from a password.

    #### Args:
    - password (str):
        Password for hashing.

    #### Returns:
    - str:
        The hash of the password.
    """
    return pwd_context.hash(password, "bcrypt")


async def admin_always_exists() -> None:
    """Create admin if it not exists."""
    dsn = settings.postgres_url.replace("+asyncpg", "")
    try:
        conn: Connection = await asyncpg.connect(dsn)
        admin = await conn.fetchrow(
            """
        SELECT id
        FROM auth
        WHERE user_type = $1
        """,
            UserType.ADMIN,
        )
        if admin is not None:
            return

        email = settings.admin_email
        password = get_hash_password(
            settings.admin_password.get_secret_value()
        )
        await conn.execute(
            """
        INSERT INTO auth(email, password, user_type, is_active)
        VALUES ($1, $2, $3, $4)
        """,
            email,
            password,
            UserType.ADMIN,
            True,
        )
    except (DataError, UniqueViolationError) as err:
        raise NoAdminException(
            "\n\n\033[101mThere is no admins for management application!\n"
            f"{err}\033[0m"
        )

    finally:
        await conn.close()
