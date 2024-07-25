import datetime
from typing import List, Optional
from pydantic import BaseModel


class ChatCreate(BaseModel):
    # id: int
    name: str = ''
    desc: Optional[str] = ''
    user_ids: Optional[List[int]] = []
    admin_ids: Optional[List[int]] = []
    messages: Optional[List[int]] = []


class ChatUpdate(BaseModel):
    id: int
    name: Optional[str]
    desc: Optional[str]
    user_ids: Optional[List[int]]
    admin_ids: Optional[List[int]]
    messages: Optional[List[int]]


class ChatDelete(BaseModel):
    id: int


class MessageCreate(BaseModel):
    user_id: int
    chat_id: int
    message: str
    date: datetime.datetime