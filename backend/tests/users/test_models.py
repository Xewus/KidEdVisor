"""The data to be written to the database must be pre-checked!
The database creates the `id` itself.
"""
import pytest

from src.users import ParentModel
from tests.conftest import get_test_db


@pytest.mark.models
def test_parent_model_attrs():
    assert ParentModel.__tablename__ == "parent"
    assert set(col.name for col in ParentModel.__table__.columns) == {
        "id",
        "name",
        "surname",
        "patronic",
        "born",
        "auth_id",
    }


@pytest.mark.models
@pytest.mark.parametrize(
    "parent",
    [
        # 0-full parent
        {
            "name": "TestName",
            "surname": "TestSurname",
            "patronic": "TestPatronic",
            "born": 123,
        },
        # 1-partial parent
        {
            "surname": "TestSurname",
            "born": 123,
        },
        # 2-empty parent
        {},
    ],
)
async def test_parent_model_create(parent: dict[str, str | int]):
    db = await anext(get_test_db())

    model = ParentModel(**parent)
    db.add(model)
    await db.flush()
    await db.refresh(model)

    assert isinstance(model.id, int)
    assert model.auth_id is None
    for field, value in parent.items():
        assert getattr(model, field) == value

    await db.close()
