import logging
from http.client import OK
from typing import BinaryIO

import requests
from requests.exceptions import ConnectionError

from settings import AZM_COMMON_SEARCH_URL


async def file_upload(file: BinaryIO, filename: str) -> bool:
    result = False
    url = ''.join((AZM_COMMON_SEARCH_URL, 'file/'))
    try:
        files = {'file': (filename, file.read())}
        response = requests.post(url, files=files)
        if response.status_code == OK:
            logging.debug(f'AZM_COMMON_SEARCH {url}\nStatusCode {str(response.status_code)}: {response.text}')
            result = True
        else:
            logging.critical(
                f'Ошибка запроса к AZM_COMMON_SEARCH {url}\nStatusCode {str(response.status_code)}: {response.text}')
    except ConnectionError as e:
        logging.critical(f'Ошибка подключения к AZM_COMMON_SEARCH {url}\n{str(e)}')

    return result
