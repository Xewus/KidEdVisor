"""The data to be written to the database must be pre-checked!
The database creates the `id` itself.
"""
import pytest
from pydantic.error_wrappers import ValidationError
from sqlalchemy import select
from src.authentication import AuthModel, TempUserModel
from src.core.enums import TableNames, UserType
from src.parents import ParentModel
from src.providers import OwnerModel
from tests.conftest import get_test_db

pytestmark = pytest.mark.usefixtures("clean_db")


@pytest.mark.models
def test_temp_user_model():
    """This model is inherited from `pydantic` BaseModel."""
    assert TempUserModel.__fields__.keys() == {
        "user_type",
        "email",
        "password",
    }, "unexpected fields in `TempUserModel`"
    # full data
    temp_user = TempUserModel(
        user_type=UserType.PARENT,
        email="test@gmail.com",
        password="qscESZ123",
    )
    assert temp_user.user_type == UserType.PARENT
    assert temp_user.email == "test@gmail.com"
    assert temp_user.password == "qscESZ123"

    # default user_type
    temp_user = TempUserModel(email="test@gmail.com", password="qscESZ123")
    assert (
        temp_user.user_type == UserType.PARENT
    ), "default type of user must be `parent`."
    assert temp_user.email == "test@gmail.com"
    assert temp_user.password == "qscESZ123"

    # mormalize email
    temp_user = TempUserModel(email="TEST@gMail.com", password="qscESZ123")
    assert temp_user.user_type == UserType.PARENT
    assert (
        temp_user.email == "test@gmail.com"
    ), "all emails must be in lowercase."
    assert temp_user.password == "qscESZ123"

    # another user_type
    temp_user = TempUserModel(
        user_type=UserType.OWNER,
        email="test@gmail.com",
        password="qscESZ123",
    )
    assert temp_user.user_type == UserType.OWNER
    assert temp_user.email == "test@gmail.com"
    assert temp_user.password == "qscESZ123"

    # bad email
    with pytest.raises(ValidationError):
        TempUserModel(email="test@gmailcom", password="qscESZ123")

    # bad password
    with pytest.raises(ValidationError):
        TempUserModel(email="test@gmail.com", password="11111111")

    # no admin registrations
    with pytest.raises(ValidationError):
        TempUserModel(
            user_type=UserType.ADMIN,
            email="test@gmail.com",
            password="qscESZ123",
        )


@pytest.mark.models
def test_auth_model_attrs():
    assert (
        AuthModel.__tablename__ == TableNames.AUTH
    ), "unexpected table name for `AuthModelodel`"
    assert set(col.name for col in AuthModel.__table__.columns) == {
        "id",
        "user_type",
        "password",
        "email",
        "is_active",
    }, "Unexpected fields in the `AuthModel`"


@pytest.mark.models
@pytest.mark.parametrize(
    "reg_data",
    [
        # 0 default type
        {
            "password": "qscvbgrey",
            "email": "test@gmail.com",
        },
        # 1 parent type
        {
            "user_type": UserType.PARENT.value,
            "password": "qscvbgrey",
            "email": "test@gmail.com",
        },
        # 2 owner type
        {
            "user_type": UserType.OWNER.value,
            "password": "qscvbgrey",
            "email": "test@gmail.com",
        },
    ],
)
async def test_auth_model_create(reg_data: dict):
    try:
        db = await anext(get_test_db())

        model = AuthModel(**reg_data)
        db.add(model)
        await db.flush()
        await db.refresh(model)

        assert isinstance(model.id, int)
        for field, value in reg_data.items():
            assert getattr(model, field) == value
        if not reg_data.get("user_type"):
            assert getattr(model, "user_type") == UserType.PARENT
    finally:
        await db.close()


@pytest.mark.models
@pytest.mark.parametrize(
    "reg_data, Model",
    [
        # 0 default auth
        (
            {
                "password": "qscvbgrey",
                "email": "test@gmail.com",
            },
            ParentModel,
        ),
        # 1 parent auth
        (
            {
                "user_type": UserType.PARENT.value,
                "password": "qscvbgrey",
                "email": "test@gmail.com",
            },
            ParentModel,
        ),
        # 2 owner auth
        (
            {
                "user_type": UserType.OWNER.value,
                "password": "qscvbgrey",
                "email": "test@gmail.com",
            },
            OwnerModel,
        ),
    ],
)
async def test_auth_trigger(reg_data: dict, Model: ParentModel | OwnerModel):
    """When a new entry is created in the `auth` table,
    a new entry must be created in the corresponding table.
    """
    auth = AuthModel(**reg_data)
    try:
        db = await anext(get_test_db())
        assert len((await db.execute(select(Model))).all()) == 0

        db.add(auth)
        await db.flush()
        models = (await db.scalars(select(Model))).all()
        assert len(models) == 1

        await db.refresh(auth)
        assert isinstance(
            await db.scalar(select(Model).where(Model.auth_id == auth.id)),
            Model,
        )
        assert models[0].auth_id == auth.id
    finally:
        await db.close()
