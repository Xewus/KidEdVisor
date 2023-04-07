from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.enums import TableNames
from src.core.mixins.models import HumanTable
from src.db.postgres.database import Base


class ParentModel(Base, HumanTable):
    """Table for parent data.

    #### Attrs:
    - id (int):
        Identifier.    #### Attrs:
    - name: (str | None):
        Real user's name.
    - surname: (str | None):
        Real user's last name.
    - patronic: (str | None):
        Real user's patronic name.
    - born: (int | None):
        User's date of birth as UNIX time.
    - auht_id (int | None):
        Relation to athenticated data.
        If None, the user is considered deleted.
    """

    __tablename__ = TableNames.PARENT

    auth_id: Mapped[int | None] = mapped_column(Integer, default=None)
