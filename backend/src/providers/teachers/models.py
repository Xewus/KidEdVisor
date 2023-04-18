from sqlalchemy import Column, ForeignKey, Integer
from src.core.enums import TableNames
from src.db.postgres import Base


class TeacherModel(Base):
    __tablename__ = TableNames.TEACHER

    owner_id = Column(
        Integer,
        ForeignKey(TableNames.OWNER + ".id", ondelete="SET DEFAULT"),
        default=None,
    )
