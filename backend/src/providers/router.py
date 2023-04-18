from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.authentication.models import AuthModel
from src.authentication.security import get_token_user
from src.core.exceptions import (
    BadRequestException,
    UnprocessableEntityException,
)
from src.db.postgres import get_db
from src.geo import PhoneModel, phone_crud

from .dependecies import get_token_empty_owner
from .intitutions.crud import institution_crud
from .intitutions.models import InstitutionModel
from .intitutions.schemes import CreateInstitutionScheme
from .owners.crud import owner_crud
from .owners.models import OwnerModel
from .owners.shemes import ResponseOwnerScheme, UpdateOwnerScheme

router = APIRouter()

NOT_IMPLEMENTED = {"This func": "Not implemented"}


@router.get(
    path="/me",
    summary="View a personal profile",
    response_model=ResponseOwnerScheme,
)
async def watch_me(
    owner: OwnerModel = Depends(get_token_empty_owner),
):
    return owner


@router.patch(
    path="/me",
    summary="Update a personal profile",
    response_description="Successful Response returns only status code 200",
)
async def update_me(
    *,
    db: AsyncSession = Depends(get_db),
    owner: OwnerModel = Depends(get_token_empty_owner),
    update_data: UpdateOwnerScheme,
):
    update_data = update_data.dict(exclude_none=True)
    if not update_data:
        return None

    _, err = await owner_crud.update(db, owner, update_data)
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
    await owner_crud.delete_auth(db, auth_user.email)
    return None


@router.get(
    path="/my_institutions",
    summary="Get a list of my institutions",
)
async def get_my_institutions(
    db: AsyncSession = Depends(get_db),
    owner: OwnerModel = Depends(get_token_empty_owner),
):
    return await institution_crud.get_many(
        db, expression=(InstitutionModel.owner_id == owner.id)
    )


@router.post(
    path="/my_institutions",
    summary="Create my new institution",
)
async def create_my_institution(
    *,
    db: AsyncSession = Depends(get_db),
    owner: OwnerModel = Depends(get_token_empty_owner),
    institution: CreateInstitutionScheme,
):
    if phones := await phone_crud.get_many(
        db,
        limit=3,
        expression=PhoneModel.number.in_(institution.address.phones),
    ):
        raise BadRequestException(
            f"numbers {[phone.number for phone in phones]} are busy"
        )

    institution.owner_id = owner.id
    return await institution_crud.create(db, institution)


@router.patch(
    path="/my_institutions",
    summary="Update my institution",
)
async def update_my_institution(
    *,
    db: AsyncSession = Depends(get_db),
    owner: OwnerModel = Depends(get_token_empty_owner),
    institution: CreateInstitutionScheme,
):
    return NOT_IMPLEMENTED


@router.delete(
    path="/my_institutions",
    summary="Delete my institution",
)
async def delete_my_institution(
    *,
    db: AsyncSession = Depends(get_db),
    owner: OwnerModel = Depends(get_token_empty_owner),
    institution: CreateInstitutionScheme,
):
    return NOT_IMPLEMENTED
