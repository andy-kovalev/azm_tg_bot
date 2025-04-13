import logging
from http.client import OK

import requests
from requests.exceptions import ConnectionError

from settings import AZM_COMMON_SEARCH_URL


async def search(search_text: str):
    result_list = []
    url = ''.join((AZM_COMMON_SEARCH_URL, 'search/'))
    try:
        response = requests.get(url, {"text": search_text})
        if response.status_code == OK:
            result_list = response.json()
        else:
            logging.critical(
                f'Ошибка запроса к AZM_COMMON_SEARCH {url}\nStatusCode {str(response.status_code)}: {response.text}')
    except ConnectionError as e:
        logging.critical(f'Ошибка подключения к AZM_COMMON_SEARCH {url}\n{str(e)}')

    return result_list
