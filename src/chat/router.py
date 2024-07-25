import json
import time
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException, HTTPException, Body
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.chat.models import Chat, Message
from src.chat.schemas import ChatCreate
from src.database import get_async_session
from src.depends import current_user

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

templates = Jinja2Templates(directory='templates')


async def get_user_from_cookie(websocket: WebSocket, user_manager=Depends(get_user_manager)):
    cookie = websocket.cookies.get("log")
    user = await auth_backend.get_strategy().read_token(cookie, user_manager)
    if not user or not user.is_active:
        raise WebSocketException("User is not active")
    yield user


@router.get('/')
async def get_user_chats(request: Request, data_current_user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    query = select(Chat.id, Chat.name).where(Chat.id.in_(data_current_user.chat_ids))
    result = await session.execute(query)
    chats = result.fetchall()

    return templates.TemplateResponse('chats.html', {'request': request, 'my_username': data_current_user.username,
                                                     'chats': chats})


@router.get('/')
async def search_chats(request: Request, data_current_user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    pass

@router.post('/')
async def create_chat(new_chat_name: str = Body(...), data_current_user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    new_chat = ChatCreate(name=new_chat_name)
    new_chat.user_ids.append(data_current_user.id)
    new_chat.admin_ids.append(data_current_user.id)
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

    return {'message': f'Chat {new_chat_name} created'}


@router.delete('/')
async def delete_chat(chat_id: int = Chat.id, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
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
async def get_chat(request: Request, chat_id: int, session: AsyncSession = Depends(get_async_session),
                   current_user: User = Depends(current_user)):
    chat = await session.get(Chat, chat_id)
    if current_user.id in chat.user_ids:
        user_ids = chat.user_ids
        admin_ids = chat.admin_ids
        users = []
        admins = []
        for user_id in user_ids:
            user = await session.get(User, user_id)
            users.append(user)
        for admin_id in admin_ids:
            admin = await session.get(User, admin_id)
            admins.append(admin)

        return templates.TemplateResponse('chat.html', {'request': request, 'chat': chat,
                                                        'users': users, 'admin_ids': admin_ids,
                                                        'current_user': current_user})
    else:
        raise HTTPException(status_code=403, detail='You are not in the chat')


@router.patch('/{chat_id}/{username}')
async def invite_user(chat_id: int, username: str, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    chat = await session.get(Chat, chat_id)
    if user.id in chat.user_ids:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.id in chat.user_ids:
            raise HTTPException(status_code=400, detail="User already in chat")

        chat_ids = user.chat_ids
        chat_ids.append(chat_id)
        stmt_user = update(User).where(User.username == username).values(chat_ids=chat_ids)

        user_ids = chat.user_ids
        user_ids.append(user.id)
        stmt_chat = update(Chat).where(Chat.id == chat_id).values(user_ids=user_ids)

        await session.execute(stmt_user)
        await session.execute(stmt_chat)
        await session.commit()

        return {"message": f"User {username} added to chat"}
    else:
        raise HTTPException(status_code=403, detail="You are not in the chat")


@router.patch('/{chat_id}/kick/{username}')
async def kick_user(chat_id: int, username: str, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    chat = await session.get(Chat, chat_id)
    if user.id in chat.admin_ids:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.id not in chat.user_ids:
            raise HTTPException(status_code=400, detail="User not in chat")
        if chat_id not in user.chat_ids:
            raise HTTPException(status_code=400, detail="User not in chat")

        chat_ids = user.chat_ids
        chat_ids.remove(chat_id)
        stmt_user = update(User).where(User.username == username).values(chat_ids=chat_ids)

        user_ids = chat.user_ids
        user_ids.remove(user.id)
        stmt_chat = update(Chat).where(Chat.id == chat_id).values(user_ids=user_ids)

        await session.execute(stmt_user)
        await session.execute(stmt_chat)
        await session.commit()
        return {"message": f"User {username} kicked from chat"}
    else:
        raise HTTPException(status_code=403, detail="You can't kick users from chat")


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


@router.websocket('/{chat_id}/ws')
async def websocket_endpoint(websocket: WebSocket, user: User = Depends(get_user_from_cookie),
                             session: AsyncSession = Depends(get_async_session),
                             chat: Chat = Depends(get_chat)):
    await manager.connect(websocket)
    chat_id = chat.id
    date = datetime.now()
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                'username': user.username,
                'message': data,
                'time': date.strftime("%H:%M")
            }
            await manager.broadcast(json.dumps(message))
            new_message = Message(chat_id=chat_id, user_id=user.id, message=data, date=date)
            stmt = insert(Message).values(**new_message.dict())
            result = await session.execute(stmt)
            
            new_message_id = result.inserted_primary_key[0]
            stmt = update(Chat).where(Chat.id == chat_id).values(messages=new_message_id)
            await session.execute(stmt)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await session.commit()

