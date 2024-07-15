import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

# from src.auth.models import
from conftest import client, async_session_maker


def test_register():
    response = client.post('/auth/register', json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "chat_ids": []
    })

    assert response.status_code == 201
