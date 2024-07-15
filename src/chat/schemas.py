from typing import List, Optional
from pydantic import BaseModel


class ChatCreate(BaseModel):
    # id: int
    name: str = ''
    desc: Optional[str] = ''
    user_ids: Optional[List[int]] = []
    messages: Optional[List[int]] = []


class ChatUpdate(BaseModel):
    id: int
    name: Optional[str]
    desc: Optional[str]
    user_ids: Optional[List[int]]
    messages: Optional[List[int]]


class ChatDelete(BaseModel):
    id: int
