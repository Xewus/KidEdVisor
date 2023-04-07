from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.postgres.crud import CRUD

from .models import InstitutionModel


class InstitutionCRUD(CRUD):
    model: InstitutionModel

    async def create(
        self,
        db: AsyncSession,
        new_obj: dict,
        need_refresh: bool = False,
    ) -> tuple[InstitutionModel, None] | tuple[None, str]:
        return await super().create(db, new_obj, need_refresh)
