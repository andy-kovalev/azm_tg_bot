from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.const.const_message import HELP_TEXT
from bot.handlers.h00_command import cmd_answer_command
from bot.message_filters import filter_chat_type_private

h_cmd_help = 'help'


async def cmd_help(message: types.Message, state: FSMContext):
    return await cmd_answer_command(message, state, h_cmd_help, HELP_TEXT)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_help, Command(h_cmd_help), filter_chat_type_private)
