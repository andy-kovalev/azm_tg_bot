# tests/test_user_utils.py
from datetime import datetime

import pytest
from aiogram.types import User, Message, Chat

from bot.utils.user import get_user_info


@pytest.fixture
def mock_message():
    """Фикстура для создания mock-сообщения"""

    def create_mock_message(user_id, username, first_name, last_name):
        user = User(id=user_id, username=username, first_name=first_name, last_name=last_name, is_bot=False)
        return Message(message_id=1, from_user=user, chat=Chat(id=0, type='private'), date=datetime.now())

    return create_mock_message


@pytest.mark.asyncio
async def test_get_user_info_complete(mock_message):
    """Тестирование получения информации о пользователе со всеми данными"""
    message = mock_message(123, "john_doe", "John", "Doe")
    user_info = await get_user_info(message)
    assert user_info == {'id': '123', 'username': 'john_doe', 'name': 'John Doe'}


@pytest.mark.asyncio
async def test_get_user_info_missing_last_name(mock_message):
    """Тестирование при отсутствии фамилии"""
    message = mock_message(456, "jane", "Jane", None)
    user_info = await get_user_info(message)
    assert user_info == {'id': '456', 'username': 'jane', 'name': 'Jane -'}


@pytest.mark.asyncio
async def test_get_user_info_missing_username(mock_message):
    """Тестирование при отсутствии username"""
    message = mock_message(789, None, "Bob", "Smith")
    user_info = await get_user_info(message)
    assert user_info == {'id': '789', 'username': '-', 'name': 'Bob Smith'}
