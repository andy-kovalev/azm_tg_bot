import logging

import requests

from requests.exceptions import ConnectionError

from settings import AZM_COMMON_SEARCH_URL


async def search(search_text: str):
    url = ''.join((AZM_COMMON_SEARCH_URL, '/search'))
    try:
        response = requests.get(url, {"text": search_text})
        result_list = response.json()
    except ConnectionError as e:
        logging.critical(f'Ошибка подключения к AZM_COMMON_SEARCH {url}')
        result_list = []

    return result_list
