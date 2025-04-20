from aiogram.types import Message


async def get_user_info(message: Message) -> dict:
    user = message.from_user
    return {'id': str(user.id), 'username': user.username, 'name': ' '.join((user.first_name, user.last_name)).strip()}
