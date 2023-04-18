from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import CRUD
from src.geo import address_crud

from .models import InstitutionModel
from .schemes import CreateInstitutionScheme


class InstitutionCRUD(CRUD):
    """The set of `CRUD` operations for `InstitutionModel`.

    #### Methods:
    - save: tuple[Base, None] | tuple[None, str]
    - create: tuple[Base, None] | tuple[None, str]
    - get_many: list[Base]
    - get: Base | None
    - update: tuple[Base, None] | tuple[None, str]
    """

    model: InstitutionModel

    async def create(
        self,
        db: AsyncSession,
        institution: CreateInstitutionScheme,
        need_refresh: bool = False,
    ) -> tuple[InstitutionModel, None] | tuple[None, str]:
        """Create a new institution in the database.

        #### Args:
        - db (AsyncSession):
            Connecting to the database.
        - institution (CreateInstitutionScheme):
            Data to save to the database.
        - need_refresh (bool): False.
            Whether to fetch fresh data from the database.

        #### Returns:
        - tuple[InstitutionModel, None] | tuple[None, str]:
            (InstitutionModel, None) if the save is successful.
            (None, error description) if the save is not successful.
        """
        db_obj = InstitutionModel(
            **institution.dict(
                exclude_none=True, exclude={"address", "categories"}
            )
        )
        full_address = await address_crud.get_full_address(
            db, institution.address
        )
        if not full_address.address:
            full_address = await address_crud.flush_new_address(
                db, institution.address, full_address
            )

        db_obj.address_id = full_address.address.id
        db.add(db_obj)
        try:
            await db.commit()
        except IntegrityError as err:
            return None, err.args[0].split(":")[1]

        if need_refresh:
            await db.refresh(db_obj)
        return db_obj, "None", full_address


institution_crud = InstitutionCRUD(InstitutionModel)
