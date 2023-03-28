from sqlmodel import Field, Relationship

from src.authentication.models import AuthModel
from src.core.mixins import NamedTable, WithIDTable

from .schemes import BaseParentScheme


class ParentModel(NamedTable, WithIDTable, BaseParentScheme, table=True):
    """Table for parent data.

    #### Attrs:
    - id (int):
        Identifier.
    - name: (str | None):
        Real parent's name.
    - surname: (str | None):
        Real parent's last name.
    - patronic: (str | None):
        Real parent's patronic name.
    - born: (date | None):
        Parent's date of birth as UNIX time.
    - auht_id (int | None):
        Relation to athenticated data.
        If None, the user is considered deleted.
    """

    auth_id: int | None = Field(foreign_key="auth.id")

    # For sqlalchemy, not table field.
    # To load data from the `auth` table,
    # you need to call it explicitly.
    # Example: select(ParentModel, AuthuserModel)
    auth: AuthModel = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={
            "lazy": "noload",
            "uselist": False,
        },
    )
