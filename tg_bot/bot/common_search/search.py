import requests

url = 'http://127.0.0.1:8000/search'


async def search(search_text: str):
    response = requests.get(url, {"text": search_text})
    result_list = response.json()
    return result_list
