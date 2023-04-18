from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.authentication import AuthModel, ResponseAuthScheme, auth_crud
from src.core.enums import AppPaths
from src.core.exceptions import BadRequestException
from src.db.postgres import get_db
from src.parents import ResponseParentScheme, parent_crud
from src.providers import ResponseOwnerScheme, owner_crud

from .dependencies import get_admin_user

router = APIRouter(dependencies=(Depends(get_admin_user),))

auth_router = APIRouter(prefix=AppPaths.AUTH)
parent_router = APIRouter(prefix=AppPaths.PARENTS)
provider_router = APIRouter(prefix=AppPaths.PROVIDERS)


NOT_IMPLEMENTED = {"This func": "Not implemented"}


@auth_router.get(
    path="/all",
    summary="Get all authenticate data",
    description="Access for admin only",
    response_model=list[ResponseAuthScheme],
)
async def read_all_auths(
    db: AsyncSession = Depends(get_db),
    offset: int | None = 0,
    limit: int | None = Query(default=10, le=50),
    is_actve: bool | None = None,
):
    if is_actve is None:
        return await auth_crud.get_many(db, offset, limit)

    return await auth_crud.get_many(
        db, offset, limit, AuthModel.is_active == is_actve
    )


@auth_router.get(
    path="/{auth_id}",
    summary="Get authenticate data by identifier",
    description="Access for admin only",
    response_model=ResponseAuthScheme,
)
async def read_auth(*, db: AsyncSession = Depends(get_db), auth_id: int):
    auth = await auth_crud.get(db, AuthModel.id == auth_id)
    if auth is None:
        raise BadRequestException(f"data by ID `{auth_id}` doesn't exists")
    return auth


@parent_router.get(
    path="/all",
    response_model=list[ResponseParentScheme],
)
async def read_all_parents(
    db: AsyncSession = Depends(get_db),
    offset: int | None = 0,
    limit: int | None = Query(default=10, le=50),
):
    return await parent_crud.get_many(db, offset, limit)


@parent_router.get(
    path="/{user_id}",
    response_model=ResponseParentScheme,
)
async def read_parent(*, db: AsyncSession = Depends(get_db), user_id: int):
    user = await parent_crud.get(db, user_id)
    if user is None:
        raise BadRequestException(f"user with ID `{user_id}` doesn't exists")

    return user


@provider_router.get(
    path="/all",
    response_model=list[ResponseOwnerScheme],
)
async def read_all_owners(
    db: AsyncSession = Depends(get_db),
    offset: int | None = 0,
    limit: int
    | None = Query(
        default=10,
        le=50,
    ),
):
    return await owner_crud.get_many(db, offset, limit)


@provider_router.get(
    path="/{provider_id}",
)
async def read_provider():
    return NOT_IMPLEMENTED


router.include_router(auth_router)
router.include_router(parent_router)
router.include_router(provider_router)
