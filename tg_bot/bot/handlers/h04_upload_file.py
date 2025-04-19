from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext

from bot.common_search.file import file_upload
from bot.const.const_message import UPLOAD_FILE_SUCCESS_TEXT, UPLOAD_FILE_ERROR_TEXT
from bot.message_filters import filter_chat_type_private, filter_content_type_document, filter_content_admin_user


async def document_upload(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(message.chat.id, 'upload_document')
    file = await message.bot.get_file(message.document.file_id)
    io_file = await message.bot.download_file(file.file_path)
    if await file_upload(io_file, message.document.file_name):
        await message.answer(UPLOAD_FILE_SUCCESS_TEXT)
    else:
        await message.answer(UPLOAD_FILE_ERROR_TEXT)


def register_handlers(dp: Dispatcher):
    dp.message.register(document_upload, filter_chat_type_private, filter_content_type_document,
                        filter_content_admin_user)
