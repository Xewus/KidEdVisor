from fastapi import APIRouter, Depends, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authentication.models import AuthModel
from src.authentication.security import get_admin_user, get_token_user
from src.core.enums import RouteTags
from src.core.exceptions import (
    BadRequestException,
    UnprocessableEntityException,
)
from src.db.postgres.database import get_db

from .crud import parent_crud
from .dependencies import get_token_parent_auth
from .models import ParentModel
from .schemes import ResponseParentAuthScheme, UpdateParentScheme

router = APIRouter()

profile_router = APIRouter(
    tags=[RouteTags.PROFILE],
)

admin_router = APIRouter(
    tags=[RouteTags.ADMIN],
    dependencies=(Depends(get_admin_user),),
)


@profile_router.get(
    path="/me",
    summary="View a personal profile",
    response_model=ResponseParentAuthScheme,
)
async def watch_me(
    parent_auth: tuple[ParentModel, AuthModel] = Depends(
        get_token_parent_auth
    ),
):
    return ResponseParentAuthScheme.from_orm(
        parent_auth[0],
        {"email": parent_auth[1].email},
    )


@profile_router.delete(
    path="/me",
    summary="Delete a personal profile",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Successful Response returns only status code 204",
)
async def delete_me(
    db: AsyncSession = Depends(get_db),
    auth_user: AuthModel = Depends(get_token_user),
):
    await parent_crud.delete_auth(db, auth_user)
    return None


@profile_router.patch(
    path="/me",
    summary="Update a personal profile",
    status_code=status.HTTP_200_OK,
    response_description="Successful Response returns only status code 200",
)
async def update_me(
    *,
    db: AsyncSession = Depends(get_db),
    parent_auth: tuple[ParentModel, AuthModel] = Depends(
        get_token_parent_auth
    ),
    update_data: UpdateParentScheme,
):
    _, err = await parent_crud.update(
        db,
        parent_auth[0],
        update_data.dict(exclude_none=True),
    )
    if err is not None:
        raise UnprocessableEntityException(detail=err)

    return None


@admin_router.get(
    path="/all",
    response_model=list[ParentModel],
)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    offset: int | None = 0,
    limit: int | None = Query(default=10, le=50),
):
    return await parent_crud.get_many(db, offset, limit)


@admin_router.get(
    path="/{user_id}",
    response_model=ParentModel,
)
async def read_user(*, db: AsyncSession = Depends(get_db), user_id: int):
    user = await parent_crud.get(db, user_id)
    if user is None:
        raise BadRequestException(f"user with ID `{user_id}` doesn't exists")

    return user


router.include_router(profile_router)
router.include_router(admin_router)
