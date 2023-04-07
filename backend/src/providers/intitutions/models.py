from sqlalchemy import Column, ForeignKey, Integer

from src.core.enums import TableNames
from src.db.postgres.database import Base


class InstitutionModel(Base):
    __tablename__ = TableNames.INSTITUTION

    owner_id = Column(
        Integer,
        ForeignKey(TableNames.OWNER + ".id", ondelete="SET DEFAULT"),
        default=None,
    )
