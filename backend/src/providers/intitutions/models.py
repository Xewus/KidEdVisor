from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.config import Limits
from src.core.enums import TableNames
from src.db.postgres import Base


class InstitutionModel(Base):
    """Table for institution data.

    #### Attrs:
    - id (int):
        Identifier.
    - name (str):
        Institution name.
    - description (str | None):
        Institution description.
    - site (str | None):
        Institution web-site.
    - address_id (int):
        Institution address ID. Relation to table `address`.
    - owner_id (int | None):
        Institution owner ID. Relation to table `owner`.
    """

    # TODO: Add categories.

    __tablename__ = TableNames.INSTITUTION

    name: Mapped[str] = mapped_column(
        String(Limits.MAX_LEN_PROVIDER_NAME),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(Limits.MAX_LEN_PROVIDER_DESCRIPTION)
    )
    site: Mapped[str | None] = mapped_column(
        String(Limits.MAX_LEN_HTTP_URL),
        default=None,
    )
    address_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(TableNames.ADDRESS + ".id"),
        nullable=False,
    )
    owner_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(TableNames.OWNER + ".id", ondelete="SET DEFAULT"),
        default=None,
    )
