"""
Настройки для работы

Пользовательская настройка производится в файле конфигурации в формате .env

Файл .env может иметь любое имя, чтобы скрипт настройки использовал файл
необходимо
  - либо указать значение в переменной окружения ENV_FILENAME
  - либо указать этот файл в параметре командной строки --envfile {файл}

По умолчанию используется файл .env
"""

import logging
from datetime import datetime
from os import path, getenv

from dotenv import load_dotenv


def configure_logging(log_file_name, log_level):
    """
    Настройка логирования
    """
    handlers = []
    if log_file_name:
        file_log = logging.FileHandler(log_file_name, encoding='utf-8')
        handlers.append(file_log)
    console_out = logging.StreamHandler()
    handlers.append(console_out)

    logging.basicConfig(handlers=handlers, level=log_level, format='%(asctime)s %(levelname)s: %(name)s: %(message)s')


def get_env_param(name: str, required: bool = False, default=None, log_text=None):
    result = getenv(name, default=default if default else None)
    if required and not result:
        exit('%s %s: root: settings: %s не задан' % (
            datetime.now().isoformat(sep=' ', timespec='milliseconds'), logging.getLevelName(logging.CRITICAL), name))
    else:
        logging.debug('settings: %s=%s', name, log_text if log_text else result)
    return result


def get_int_env_param(name: str, required: bool = False, default=None, log_text=None) -> int | str:
    result = get_env_param(name, required, default, log_text)
    if result.isdigit():
        result = int(result)
    else:
        logging.error('settings: %s=%s, не является числом', name, log_text if log_text else result)
    return result


def get_obfuscate_env_param_value(value):
    def fill_asterisk(fill_count):
        return '*' * fill_count

    if len(value) > 3:
        inx = 1 if len(value) < 9 else 3
        return value[:inx] + fill_asterisk(len(value) - inx * 2) + value[-inx:]
    else:
        return fill_asterisk(len(value))


def get_connect_uri(protocol, resource, address, port=None, user=None, password=None) -> str:
    """
    Формирует URL для подключения к сервисам
    :param protocol: протокол подключения (redis, mongodb, http)
    :param resource: ресурс подключения (db_number, db_name, endpoint)
    :param address: адрес
    :param port: порт
    :param user: имя пользователя
    :param password: пароль пользователя
    :return: URI подключения к в формате protocol://[user:password@]address[:port]/resource
    """
    user_str = f'{user}{f":{password}" if password else ""}@' if user else ''
    port_str = f':{port}' if port else ''

    return '%s://%s%s%s/%s' % (protocol, user_str, address, port_str, resource) if address else ''


# .env файл для загрузки параметров
ENV_FILENAME = path.abspath(getenv('ENV_FILENAME', default='.env'))
if path.exists(ENV_FILENAME) and path.isfile(ENV_FILENAME):
    load_dotenv(ENV_FILENAME)
else:
    exit('%s %s: root: settings: environment variable ENV_FILENAME=%s, файл не найден' % (
        datetime.now().isoformat(sep=' ', timespec='milliseconds'), logging.getLevelName(logging.CRITICAL),
        ENV_FILENAME))

# logging param
# Имя файла для записи логов
LOG_FILE_NAME = path.abspath(getenv('LOG_FILE_NAME', default='azm_tg_bot.log'))

# Уровень записи логов ERROR, WARNING, DEBUG, INFO
LOG_LEVEL = logging.getLevelName(getenv('LOG_LEVEL', default='INFO'))

configure_logging(LOG_FILE_NAME, LOG_LEVEL)

logging.debug('settings: LOG_FILE_NAME=%s', LOG_FILE_NAME)
logging.debug('settings: LOG_LEVEL=%s', logging.getLevelName(LOG_LEVEL))
logging.debug('%s', '-' * 20)

# bot param
# Токен Telegram бота
BOT_TOKEN_OBFUSCATED = get_obfuscate_env_param_value(getenv('BOT_TOKEN'))
BOT_TOKEN = get_env_param('BOT_TOKEN', required=True, log_text=BOT_TOKEN_OBFUSCATED)

logging.debug('%s', '-' * 20)

# azm_common_search param
# Адрес common_search
AZM_COMMON_SEARCH_ADDRESS = get_env_param('AZM_COMMON_SEARCH_ADDRESS', required=True)

# Порт common_search
AZM_COMMON_SEARCH_PORT = get_int_env_param('AZM_COMMON_SEARCH_PORT', default='8000')

# Вычисляемы параметр для внутреннего удобства
AZM_COMMON_SEARCH_URL = get_connect_uri('http', '', AZM_COMMON_SEARCH_ADDRESS, AZM_COMMON_SEARCH_PORT)
