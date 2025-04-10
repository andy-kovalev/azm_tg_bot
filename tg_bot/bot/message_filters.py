from aiogram.enums import ChatType, ContentType
from aiogram.types import Message, CallbackQuery


# lambda msg: msg.chat.type == ChatType.PRIVATE
def _get_message(message):
    if isinstance(message, Message):
        return message
    elif isinstance(message, CallbackQuery):
        return message.message
    else:
        return None


async def filter_chat_type_private(message) -> bool:
    msg: Message = _get_message(message)
    if msg:
        return msg.chat.type == ChatType.PRIVATE
    else:
        return False


async def filter_content_type_contact(message) -> bool:
    msg: Message = _get_message(message)
    if msg:
        return msg.content_type == ContentType.CONTACT
    else:
        return False


async def filter_content_type_text(message) -> bool:
    msg: Message = _get_message(message)
    if msg:
        return msg.content_type == ContentType.TEXT
    else:
        return False
