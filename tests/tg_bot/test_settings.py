import logging
from os import environ, path
from types import MethodType, FunctionType, ModuleType
from unittest.mock import patch

import pytest

from tg_bot import settings

EXCLUDE_PARAM = 'EXCLUDE'


@pytest.fixture(autouse=True)
def default_test_settings() -> dict:
    """
    Значения по умолчанию для параметров из settings.py

    Если в дальнейшем необходимо пропустить проверку параметра, нужно указать значение EXCLUDE_PARAM
    (например для вычислимых параметров)
    :return: словарь параметров со значениями по умолчанию
    """
    return {"ENV_FILENAME": ".env",
            "LOG_FILE_NAME": path.abspath("azm_tg_bot.log"),
            "LOG_LEVEL": EXCLUDE_PARAM,
            "BOT_TOKEN": "",
            "BOT_TOKEN_OBFUSCATED": EXCLUDE_PARAM,
            "AZM_COMMON_SEARCH_ADDRESS": "",
            "AZM_COMMON_SEARCH_PORT": "8000",
            "AZM_COMMON_SEARCH_URL": EXCLUDE_PARAM
            }


@pytest.fixture(autouse=True)
def test_env_settings():
    env_filename_param = 'ENV_FILENAME'
    env_filename = path.abspath(environ.get(env_filename_param))
    env_vars = {env_filename_param: env_filename}
    with open(env_filename, mode='r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            env_vars.update({key: value})

    return env_vars


def test_get_env_param(monkeypatch):
    test_param_name = 'TEST_PARAM_NAME'
    test_param_value = 'test_param_value'
    test_param_default_value = 'test_param_default_value'

    test_result = settings.get_env_param(test_param_name, default=test_param_default_value)
    assert test_result == test_param_default_value

    monkeypatch.setenv(test_param_name, test_param_value)
    with patch('logging.Logger.debug') as mocked_logger:
        test_result = settings.get_env_param(test_param_name, default=test_param_default_value)
        mocked_logger.assert_called_once()
    assert test_result == test_param_value

    monkeypatch.setenv(test_param_name, '')
    with pytest.raises(SystemExit) as exc_info:
        settings.get_env_param(test_param_name, required=True)
    assert str(exc_info.value.code).find(logging.getLevelName(logging.CRITICAL)) > 0


@pytest.mark.parametrize(['param', 'result'], (
        ('1234567890', '123****890'),
        ('123456', '1****6'),
        ('123', '***'),
        (None, '')))
def test_get_obfuscate_env_param_value(param, result):
    obfuscate_token = settings.get_obfuscate_env_param_value(param)

    assert obfuscate_token == result


@pytest.mark.parametrize(['db_number', 'address', 'port', 'user', 'password', 'result'], (
        ('5', 'address.local', '', '', '', 'redis://address.local/5'),
        ('5', 'address.local', '6379', '', '', 'redis://address.local:6379/5'),
        ('5', 'address.local', '6379', 'user', 'password', 'redis://user:password@address.local:6379/5')))
def test_get_connect_uri(db_number, address, port, user, password, result):
    connect_uri = settings.get_connect_uri('redis', db_number, address, port, user, password)

    assert connect_uri == result


def test_settings_params(test_env_settings, default_test_settings):
    env_vars = test_env_settings

    settings_param = [v for v in vars(settings) if not isinstance(getattr(settings, v), (
        type, MethodType, FunctionType, ModuleType)) and not v.startswith('__')]

    for param in settings_param:
        if param in default_test_settings.keys():
            if default_test_settings[param] == EXCLUDE_PARAM:
                continue

        if param not in env_vars.keys() and param not in default_test_settings.keys() and str(
                default_test_settings[param]) == '':
            pytest.fail(f'Атрибут {param} добавлен в settings.py и не указан в .env файле '
                        'или default_test_settings() фикстуре')
        elif param not in env_vars.keys() and param in default_test_settings.keys():
            assert str(getattr(settings, param)) == str(default_test_settings[param]), (f'Атрибут {param} не '
                                                                                        'соответствует '
                                                                                        'default_test_settings() '
                                                                                        'фикстуре')
