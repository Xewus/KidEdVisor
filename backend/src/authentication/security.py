from time import time

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import Limits, settings
from src.core.enums import AppPaths, UserType
from src.core.exceptions import BadRequestException, CredentialsException
from src.db.postgres.database import ASessionMaker, get_db

from .crud import auth_crud
from .models import AuthModel
from .schemes import TokenDataScheme

token_url = f"{AppPaths.API}{AppPaths.AUTH}{AppPaths.TOKEN}"
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
    print(email, user)
    if user is None or not user.is_active:
        raise BadRequestException(f"user with email: {email} not found")

    if not pwd_context.verify(password, user.password):
        raise BadRequestException("invalid password")

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
    """Create an admin if it doesn't exist."""
    async with ASessionMaker() as db:
        db: AsyncSession
        if await db.scalar(
            select(AuthModel.id)
            .where(AuthModel.user_type == UserType.ADMIN)
            .limit(1)
        ):
            return None

        password = get_hash_password(
            settings.admin_password.get_secret_value()
        )
        admin = AuthModel(
            email=settings.admin_email,
            is_active=True,
            user_type=UserType.ADMIN,
            password=password,
        )
        db.add(admin)
        await db.commit()
        return None
