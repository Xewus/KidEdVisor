from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.core.enums import TableNames
from src.core.mixins import HumanModel
from src.db.postgres import Base


class ParentModel(Base, HumanModel):
    """Table for parent data.

    #### Attrs:
    - id (int):
        Identifier.
    - name (str | None):
        Real user's name.
    - surname (str | None):
        Real user's last name.
    - patronic (str | None):
        Real user's patronic name.
    - born (int | None):
        User's date of birth as UNIX time.
    - auht_id (int | None):
        Relation to athenticated data.
        If None, the user is considered deleted.
    """

    __tablename__ = TableNames.PARENT

    auth_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.AUTH + ".id", ondelete="SET DEFAULT"),
        default=None,
    )
