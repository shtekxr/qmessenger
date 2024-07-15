from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
SECRET = os.environ.get('SECRET')
SECRET_MANAGER = os.environ.get('SECRET_MANAGER')

DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')
DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
