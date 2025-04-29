from aiogram.types import Message


async def get_user_info(message: Message) -> dict:
    user = message.from_user
    _id = user.id if user.id else 0
    _username = user.username if user.username else '-'
    _first_name = user.first_name if user.first_name else '-'
    _last_name = user.last_name if user.last_name else '-'

    return {'id': str(_id), 'username': _username, 'name': ' '.join((_first_name, _last_name)).strip()}
