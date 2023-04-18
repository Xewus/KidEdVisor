"""The data to be written to the database must be pre-checked!
The database creates the `id` itself.
"""
import pytest
from sqlalchemy import select
from src.authentication import AuthModel
from src.core.enums import TableNames, UserType
from src.providers import OwnerModel, owner_crud
from tests.conftest import get_test_db

pytestmark = pytest.mark.usefixtures("clean_db")


@pytest.mark.models
def test_owner_model_attrs():
    assert (
        OwnerModel.__tablename__ == TableNames.OWNER
    ), "Unexpected table name for `OwnerModel`"
    assert set(col.name for col in OwnerModel.__table__.columns) == {
        "id",
        "name",
        "surname",
        "patronic",
        "born",
        "auth_id",
    }, "Unexpected fields in the `OwnerModel`"


@pytest.mark.models
async def test_owner_model_create():
    owner = {
        "name": "TestName",
        "surname": "TestSurname",
        "patronic": "TestPatronic",
        "born": 123,
    }
    db = await anext(get_test_db())

    model = OwnerModel(**owner)
    db.add(model)
    await db.flush()
    await db.refresh(model)

    assert isinstance(model.id, int)
    assert model.auth_id is None
    for field, value in owner.items():
        assert getattr(model, field) == value

    await db.close()


@pytest.mark.crud
async def test_delete_owner():
    """The owner should not be removed,
    only the associated row in the `auth` table should be removed.
    """
    db = await anext(get_test_db())
    try:
        assert len((await db.execute(select(OwnerModel))).all()) == 0
        assert len((await db.execute(select(AuthModel))).all()) == 0

        auth = AuthModel(
            email="test@mail.test",
            password="1qaz2wsx",
            user_type=UserType.OWNER.value,
        )
        db.add(auth)
        await db.flush()
        owner = await db.scalar(
            select(OwnerModel).where(OwnerModel.auth_id == auth.id)
        )
        assert isinstance(owner, OwnerModel)

        await owner_crud.delete_auth(db, auth.email)
        await db.refresh(owner)
        assert owner.auth_id is None
        assert (
            await db.scalar(
                select(OwnerModel).where(OwnerModel.auth_id == auth.id)
            )
            is None
        )

    finally:
        await db.close()
