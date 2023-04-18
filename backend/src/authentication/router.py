from typing import Callable

from fastapi import APIRouter, BackgroundTasks, Depends, Path, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.config import Limits
from src.core.enums import AppPaths, RouteTags
from src.core.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnprocessableEntityException,
)
from src.core.utils import random_string
from src.db.postgres import get_db
from src.mail import get_send_confirm_link

from .crud import auth_crud, temp_crud
from .forms import EmailForm, Oauth2EmailForm, PasswordForm
from .models import AuthModel
from .schemes import CreateTempUserScheme, PasswordScheme, TokenScheme
from .security import (
    authenticate_user,
    create_JWT_token,
    get_hash_password,
    get_token_user,
)

router = APIRouter(prefix=AppPaths.AUTH, tags=[RouteTags.AUTH])


@router.post(
    path="/registration",
    summary="Registration a new user",
    description="User data is temporarily saved. "
    "After registration, the user receive a confirmation link to his email. "
    "The data will be deleted if the user doesn't confirm the registration.",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Successful Response returns only status code 202",
)
async def registration(
    *,
    request: Request,
    db: AsyncSession = Depends(get_db),
    send_mail: Callable = Depends(get_send_confirm_link),
    backgrond_task: BackgroundTasks,
    new_user: CreateTempUserScheme,
) -> None:
    if await auth_crud.email_exists(db, new_user.email):
        raise UnprocessableEntityException(
            f"user with email `{new_user.email}` alredy exists"
        )

    new_user.password = get_hash_password(new_user.password)
    uuid = temp_crud.set_temp_user(new_user)
    link = request.url_for("confirm_registration", uuid=uuid)._url
    backgrond_task.add_task(send_mail, new_user.email, link)
    return link  # for development. return None


@router.get(
    path="/confirm/{uuid}",
    name="confirm_registration",
    summary="User registration confirmation",
    description="The user will be removed from temporary storage and "
    "saved as a real user.",
    response_description="Successful Response returns only status code 201",
)
async def confirm_registration(
    *,
    request: Request,
    db: AsyncSession = Depends(get_db),
    uuid: str = Path(
        description="Http link suffix for user registration",
        example="993418d6434848bc927a13c48ca111f4",
        min_length=32,
        max_length=32,
    ),
) -> None:
    temp_user = temp_crud.pop_temp_user(uuid)
    if not temp_user:
        raise NotFoundException("start again please")

    _, err = await auth_crud.create(db, temp_user.dict(), True)
    if err is not None:
        raise UnprocessableEntityException(err)

    return RedirectResponse(request.base_url)


@router.post(
    path=AppPaths.TOKEN,
    summary="Get authorization token",
    description="User submits form with email password, user type and "
    "gets `JWT` token",
    response_model=TokenScheme,
)
async def login(
    db: AsyncSession = Depends(get_db),
    form: Oauth2EmailForm = Depends(),
):
    print(form)
    user = await authenticate_user(db, form.email, form.password)
    data = {"sub": user.email, "ut": user.user_type}
    return TokenScheme(access_token=create_JWT_token(data))


@router.post(
    path="/change_password",
    summary="Change password",
    description="The authorized user submits a form with a new password.",
    status_code=status.HTTP_200_OK,
    response_description="Successful Response returns only status code 200",
)
async def request_change_password(
    *,
    db: AsyncSession = Depends(get_db),
    user: AuthModel = Depends(get_token_user),
    form: PasswordForm = Depends(),
):
    user.password = get_hash_password(form.password)
    _, err = await auth_crud.save(db, user)
    if err is not None:
        raise UnprocessableEntityException(detail=err)

    return None


@router.post(
    path="/forget_password",
    summary="Get a link to create a new password",
    description="The user specifies registration email address and "
    "receives a link to this email address. "
    "Then he follows this link and receives a new password.",
)
async def forget_password(
    *,
    request: Request,
    db: AsyncSession = Depends(get_db),
    form: EmailForm = Depends(),
    send_mail: Callable = Depends(get_send_confirm_link),
    backgrond_task: BackgroundTasks,
):
    user: AuthModel = await auth_crud.get(db, AuthModel.email == form.email)
    if user is None:
        raise BadRequestException(f"user with email `{form.email}` not exists")

    if not user.is_active:
        raise ForbiddenException

    uuid = temp_crud.set_want_password(form.email)
    link = request.url_for("get_new_password", uuid=uuid)._url
    backgrond_task.add_task(send_mail, form.email, link)
    return link  # for development. return None


@router.get(
    path="/forget_password/{uuid}",
    name="get_new_password",
    summary="Get new password",
    description="The user gets here by a link from the mail and "
    "receives an automatically generated access password.",
    response_model=PasswordScheme,
)
async def get_new_password(
    *,
    db: AsyncSession = Depends(get_db),
    uuid: str = Path(
        description="Http link suffix for user registration",
        example="993418d6434848bc927a13c48ca111f4",
        min_length=32,
        max_length=32,
    ),
) -> None:
    temp_email = temp_crud.pop_want_password(uuid)
    if not temp_email:
        raise NotFoundException("start again please")

    user: AuthModel = await auth_crud.get(
        db, AuthModel.email == str(temp_email)
    )
    if user is None:
        raise BadRequestException(f"user with email `{temp_email}` not exists")

    if not user.is_active:
        raise ForbiddenException

    # WARNING: There is a chance to create a password that is too simple.
    new_password = random_string(Limits.MIN_LEN_PASSWORD)
    user.password = get_hash_password(new_password)
    _, err = await auth_crud.save(db, user)
    if err is not None:
        raise UnprocessableEntityException("please try again")

    return {"password": new_password}
