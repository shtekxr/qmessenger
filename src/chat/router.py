from typing import List

from fastapi import APIRouter, Depends, Form, WebSocket, WebSocketDisconnect, WebSocketException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.chat.models import Chat
from src.chat.schemas import ChatCreate
from src.database import get_async_session
from src.depends import current_user

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

templates = Jinja2Templates(directory='templates')





@router.get('/')
async def get_user_chats(request: Request, data_current_user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    query = select(Chat.id, Chat.name).where(Chat.id.in_(data_current_user.chat_ids))
    result = await session.execute(query)
    chats = result.fetchall()

    return templates.TemplateResponse('chats.html', {'request': request, 'my_username': data_current_user.username,
                                                     'chats': chats})


@router.post('/')
async def create_chat(new_chat_name: str = Form(...), data_current_user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    new_chat = ChatCreate(name=new_chat_name)
    new_chat.user_ids.append(data_current_user.id)
    new_chat.name = new_chat_name
    stmt = insert(Chat).values(**new_chat.dict())
    result = await session.execute(stmt)
    await session.commit()
    new_chat_id = result.inserted_primary_key[0]
    print(f'User id = {data_current_user.id}')
    print(f'Chat id = {new_chat_id}')
    data_current_user.chat_ids.append(new_chat_id)
    stmt = update(User).where(User.id == data_current_user.id).values(chat_ids=data_current_user.chat_ids)
    await session.execute(stmt)
    await session.commit()
    print(f'User chat id = {data_current_user.chat_ids}')

    return {'status': 'ok'}


@router.delete('/')
async def delete_chat(chat_id: int = Chat.id, session: AsyncSession = Depends(get_async_session)):
    chat = await session.get(Chat, chat_id)
    chat_users_query = select(User).where(User.id.in_(chat.user_ids))
    result = await session.execute(chat_users_query)
    chat_users = result.scalars().all()
    for user in chat_users:
        if chat_id in user.chat_ids:
            user.chat_ids.remove(chat_id)
            await session.commit()
    stmt = delete(Chat).where(Chat.id == chat_id)
    await session.execute(stmt)
    await session.commit()

    return {'status': 'ok'}


@router.get('/{chat_id}')
async def get_chat(request: Request, chat_id: int, session: AsyncSession = Depends(get_async_session)):
    chat = await session.get(Chat, chat_id)

    return templates.TemplateResponse('chat.html', {'request': request, 'chat': chat})


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str,websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def get_user_from_cookie(websocket: WebSocket, user_manager=Depends(get_user_manager)):
    cookie = websocket.cookies.get("log")
    user = await auth_backend.get_strategy().read_token(cookie, user_manager)
    if not user or not user.is_active:
        raise WebSocketException("User is not active")
    yield user


@router.websocket('/{chat_id}/ws')
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_user_from_cookie)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user.username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


