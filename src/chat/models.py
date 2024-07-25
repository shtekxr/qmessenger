import datetime

from sqlalchemy import Column, Integer, ARRAY, String, TIMESTAMP, MetaData, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

metadata = Base.metadata


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    user_ids: Mapped[list] = mapped_column(ARRAY(Integer))
    admin_ids: Mapped[list] = mapped_column(ARRAY(Integer))
    messages: Mapped[list] = mapped_column(ARRAY(Integer))


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
