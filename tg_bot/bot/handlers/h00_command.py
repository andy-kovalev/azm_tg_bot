import logging

from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def cmd_answer_command(message: Message, state: FSMContext, command: str, text: str):
    logging.debug('Chat[%s], Command[%s]', message.chat.id, '/%s' % command)
    await message.answer(text, parse_mode=ParseMode.HTML)
    await state.clear()


def register_handlers(dp: Dispatcher):
    pass
