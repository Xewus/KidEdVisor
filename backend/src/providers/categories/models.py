from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.enums import TableNames
from src.db.postgres import Base


class CategoryModel(Base):
    """Table for catefories of services.

    #### ttrs:
    - name (str):
        Category name.
    - description (str):
        Category description.
    """

    __tablename__ = TableNames.CATEGORY

    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
