import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from src.auth.base_config import auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from chat.router import router as router_chat

from depends import fastapi_users


app = FastAPI(
    title='QMessenger'
)

connected_users = {}

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.middleware("http")
async def redirect_to_chats_if_logged_in(request: Request, call_next):
    if request.url.path == "/" and request.cookies.get("log"):
        return RedirectResponse(url="/chats", status_code=303)
    response = await call_next(request)
    return response


'''User Read/Update Router'''

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)

'''Auth Router'''

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

'''Register Router'''

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

'''Reset Password Router'''

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(router_chat)

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def get_home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/register')
async def get_register(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


if __name__ == '__main__':
    '''Server'''
    uvicorn.run('main:app', host='0.0.0.0', port=80, reload=True)
