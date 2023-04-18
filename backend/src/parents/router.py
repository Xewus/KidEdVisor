from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.authentication import AuthModel, get_token_user
from src.core.exceptions import UnprocessableEntityException
from src.db.postgres import get_db

from .dependencies import get_token_parent
from .parents.crud import parent_crud
from .parents.models import ParentModel
from .parents.schemes import ResponseParentScheme, UpdateParentScheme

router = APIRouter()


@router.get(
    path="/me",
    summary="View a personal profile",
    response_model=ResponseParentScheme,
)
async def watch_me(
    parent: ParentModel = Depends(get_token_parent),
):
    return parent


@router.patch(
    path="/me",
    summary="Update a personal profile",
    response_description="Successful Response returns only status code 200",
)
async def update_me(
    *,
    db: AsyncSession = Depends(get_db),
    parent: ParentModel = Depends(get_token_parent),
    update_data: UpdateParentScheme,
):
    update_data = update_data.dict(exclude_none=True)
    if not update_data:
        return None

    _, err = await parent_crud.update(db, parent, update_data)
    if err is not None:
        raise UnprocessableEntityException(detail=err)

    return None


@router.delete(
    path="/me",
    summary="Delete a personal profile",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Successful Response returns only status code 204",
)
async def delete_me(
    db: AsyncSession = Depends(get_db),
    auth_user: AuthModel = Depends(get_token_user),
):
    await parent_crud.delete_auth(db, auth_user.email)
    return None
