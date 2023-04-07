"""The data to be written to the database must be pre-checked!
The database creates the `id` itself.
"""
import pytest
from pydantic.error_wrappers import ValidationError

from src.authentication.models import AuthModel, TempUserModel
from src.core.enums import UserType
from tests.conftest import get_test_db


@pytest.mark.models
def test_temp_user_model():
    assert TempUserModel.__fields__.keys() == {
        "user_type",
        "email",
        "password",
    }

    # full data
    temp_user = TempUserModel(
        user_type=UserType.PARENT,
        email="test@gmail.com",
        password="qscESZ123",
    )
    assert isinstance(temp_user.user_type, int)
    assert temp_user.user_type == UserType.PARENT

    assert isinstance(temp_user.email, str)
    assert temp_user.email == "test@gmail.com"

    assert isinstance(temp_user.password, str)
    assert temp_user.password == "qscESZ123"

    # default user_type
    temp_user = TempUserModel(email="test@gmail.com", password="qscESZ123")
    assert temp_user.user_type == UserType.PARENT
    assert temp_user.email == "test@gmail.com"
    assert temp_user.password == "qscESZ123"

    # mormalize email
    temp_user = TempUserModel(email="TEST@gMail.com", password="qscESZ123")
    assert temp_user.user_type == UserType.PARENT
    assert temp_user.email == "test@gmail.com"
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

    # not bad email
    with pytest.raises(ValidationError):
        TempUserModel(email="test@gmailcom", password="qscESZ123")

    # not bad password
    with pytest.raises(ValidationError):
        TempUserModel(email="test@gmail.com", password="11111111")

    # not admin
    with pytest.raises(ValidationError):
        TempUserModel(
            user_type=UserType.ADMIN,
            email="test@gmail.com",
            password="qscESZ123",
        )


@pytest.mark.models
def test_auth_model_attrs():
    assert AuthModel.__tablename__ == "auth"
    assert set(col.name for col in AuthModel.__table__.columns) == {
        "id",
        "user_type",
        "password",
        "email",
        "is_active",
    }


@pytest.mark.models
@pytest.mark.parametrize(
    "auth",
    [
        # 0-default auth
        {
            "password": "qscvbgrey",
            "email": "test@gmail.com",
        },
        # 1-parent auth
        {
            "user_type": UserType.PARENT.value,
            "password": "qscvbgrey",
            "email": "test@gmail.com",
        },
        # 2-owner auth
        {
            "user_type": UserType.OWNER.value,
            "password": "qscvbgrey",
            "email": "test@gmail.com",
        },
    ],
)
async def test_auth_model_create(auth: dict):
    db = await anext(get_test_db())

    model = AuthModel(**auth)
    db.add(model)
    await db.flush()
    await db.refresh(model)

    assert isinstance(model.id, int)
    for field, value in auth.items():
        assert getattr(model, field) == value

    await db.close()
