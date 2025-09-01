# tests/test_file_upload.py
import pytest
from unittest.mock import patch, MagicMock
from bot.common_search.file import file_upload


@pytest.mark.asyncio
@patch('bot.common_search.file.requests.post')
async def test_file_upload_success(mock_post):
    """Тестирование успешной загрузки файла"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    mock_file = MagicMock()
    mock_file.read.return_value = b"test content"

    result = await file_upload(mock_file, "test.xlsx")
    assert result is True
    mock_file.read.assert_called_once()
    mock_post.assert_called_once()


@pytest.mark.asyncio
@patch('bot.common_search.file.requests.post')
async def test_file_upload_failure(mock_post):
    """Тестирование неудачной загрузки файла (ошибка сервера)"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    mock_file = MagicMock()
    result = await file_upload(mock_file, "test.xlsx")
    assert result is False


@pytest.mark.asyncio
@patch('bot.common_search.file.requests.post', side_effect=ConnectionError)
async def test_file_upload_connection_error(mock_post):
    """Тестирование ошибки соединения при загрузке файла"""
    mock_file = MagicMock()
    with pytest.raises(ConnectionError):
        result = await file_upload(mock_file, "test.xlsx")
        assert result is False
