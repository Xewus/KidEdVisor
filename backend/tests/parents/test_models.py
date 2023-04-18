"""The data to be written to the database must be pre-checked!
The database creates the `id` itself.
"""
import pytest
from sqlalchemy import select
from src.authentication import AuthModel
from src.core.enums import TableNames
from src.parents import ParentModel, parent_crud
from tests.conftest import get_test_db

pytestmark = pytest.mark.usefixtures("clean_db")


@pytest.mark.models
def test_parent_model_attrs():
    assert (
        ParentModel.__tablename__ == TableNames.PARENT
    ), "Unexpected table name for `ParentModel`"
    assert set(col.name for col in ParentModel.__table__.columns) == {
        "id",
        "name",
        "surname",
        "patronic",
        "born",
        "auth_id",
    }, "unexpected fields in the `ParentModel`"


@pytest.mark.models
@pytest.mark.parametrize(
    "parent",
    [
        # 0 full parent
        {
            "name": "TestName",
            "surname": "TestSurname",
            "patronic": "TestPatronic",
            "born": 123,
        },
        # 1 partial parent
        {
            "surname": "TestSurname",
            "born": 123,
        },
        # 2 empty parent
        {},
    ],
)
async def test_parent_model_create(parent: dict[str, str | int]):
    db = await anext(get_test_db())

    model = ParentModel(**parent)
    try:
        db.add(model)
        await db.flush()

        assert isinstance(model.id, int)
        assert model.auth_id is None
        for field, value in parent.items():
            assert getattr(model, field) == value
    finally:
        await db.close()


@pytest.mark.crud
async def test_delete_parent():
    """The parent should not be removed,
    only the associated row in the `auth` table should be removed.
    """
    db = await anext(get_test_db())
    try:
        assert not (await db.execute(select(ParentModel))).all()
        assert not (await db.execute(select(AuthModel))).all()

        auth = AuthModel(email="test@mail.test", password="1qaz2wsx")
        db.add(auth)
        await db.flush()
        parent = await db.scalar(
            select(ParentModel).where(ParentModel.auth_id == auth.id)
        )
        assert isinstance(parent, ParentModel)

        await parent_crud.delete_auth(db, auth.email)
        await db.refresh(parent)
        assert parent.auth_id is None
        assert (
            await db.scalar(
                select(ParentModel).where(ParentModel.auth_id == auth.id)
            )
            is None
        )

    finally:
        await db.close()
