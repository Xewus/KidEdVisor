from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.postgres.database import get_db

router = APIRouter()

NOT_IMPLEMENTED = {"This func": "Not implemented"}


@router.get(path="/me")
async def watch_me():
    return NOT_IMPLEMENTED


@router.patch(
    path="/update",
)
async def update_me():
    return NOT_IMPLEMENTED


@router.delete(
    path="/delete",
)
async def delete_me():
    return NOT_IMPLEMENTED


@router.get(
    path="/",
)
async def get_all_providers(
    db: AsyncSession = Depends(get_db),
    offset: int | None = 0,
    limit: int
    | None = Query(
        default=10,
        le=50,
    ),
):
    return NOT_IMPLEMENTED


@router.get(
    path="/{user_id}",
)
async def read_provider():
    return NOT_IMPLEMENTED
