from sqlmodel import Field, SQLModel

from src.db.postgres.crud import CRUD


class TutorModel(SQLModel, table=True):
    __tablename__ = "tutor"

    id: int | None = Field(
        primary_key=True,
    )


class TutorCRUD(CRUD):
    ...


class InstitutionModel(SQLModel, table=True):
    __tablename__ = "institution"

    id: int | None = Field(
        primary_key=True,
    )


class InstitutionCRUD(CRUD):
    ...


tutor_crud = TutorCRUD(TutorModel)
institution_crud = InstitutionCRUD(InstitutionModel)
