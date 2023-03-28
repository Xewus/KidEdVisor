import pytest
from pydantic.error_wrappers import ValidationError

from src.authentication.models import AuthModel, TempUserModel
from src.core.enums import UserType


@pytest.mark.registration
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
        user_type=UserType.TEACHER,
        email="test@gmail.com",
        password="qscESZ123",
    )
    assert temp_user.user_type == UserType.TEACHER
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


@pytest.mark.registration
def test_auth_model():
    """The data to be written to the database must be pre-checked!
    The database creates the `id` itself.
    """
    assert AuthModel.__tablename__ == "auth"
    assert AuthModel.__fields__.keys() == {
        "id",
        "user_type",
        "password",
        "email",
        "is_active",
    }

    auth_user = AuthModel(
        user_type=UserType.PARENT,
        password="qscvbgrey",
        email="test@gmail.com",
    )

    assert isinstance(auth_user.id, int | None)
    assert auth_user.id is None

    assert isinstance(auth_user.user_type, int)
    assert auth_user.user_type == UserType.PARENT

    assert isinstance(auth_user.password, str)
    assert auth_user.password == "qscvbgrey"

    assert isinstance(auth_user.email, str)
    assert auth_user.email == "test@gmail.com"

    assert isinstance(auth_user.is_active, bool | None)
    assert not auth_user.is_active
