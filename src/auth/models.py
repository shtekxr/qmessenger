from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

metadata = Base.metadata


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False)
    chat_ids: Mapped[list] = mapped_column(ARRAY(Integer), default=[])
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False, default='')
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False, default='')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
