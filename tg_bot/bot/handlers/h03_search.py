from aiogram import types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot.common_search import search
from bot.const.const_message import NOT_FOUND_SEARCH_TEXT, MAX_FOUND_SEARCH_COUNT, MAX_FOUND_SEARCH_TEXT, \
    AVAILABLE_TEXT, NOT_AVAILABLE_TEXT, PRICE_ITEM_TEXT
from bot.message_filters import filter_chat_type_private, filter_content_type_text, filter_content_admin_user
from bot.utils.text import mdv2_escape
from bot.utils.user import get_user_info
from settings import search_logging, SEARCH_LOG_SEPARATOR, SEARCH_LOG_FILE_NAME


async def log_download(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(message.chat.id, 'upload_document')
    search_log_file = FSInputFile(SEARCH_LOG_FILE_NAME, filename='tg_bot_search.log')
    await message.answer_document(search_log_file, caption='Лог запросов к боту')


async def txt_search(message: types.Message, state: FSMContext):
    if await filter_content_admin_user(message) and message.text.upper() in (
            'LOG', 'STAT', 'СТАТИСТИКА', 'ЛОГ', 'ЛОГИ', 'REQUESTS', 'ЗАПРОСЫ'):
        await log_download(message, state)
    else:
        user_info = await get_user_info(message)

        result_message_text = NOT_FOUND_SEARCH_TEXT
        search_text = message.text

        search_logging().info(
            SEARCH_LOG_SEPARATOR.join(('>', user_info['id'], user_info['username'], user_info['name'], search_text)))

        result_search_count = 0
        if search_text:
            result_search_list = await search.search(search_text)
            if len(result_search_list) > 0:
                result_message_text = ''
                search_item_count = 0
                for search_item in result_search_list:
                    items_text = ''
                    available_count = search_item['available_count']
                    available_text = NOT_AVAILABLE_TEXT
                    if available_count and isinstance(available_count, (int, float)) and available_count > 0:
                        available_text = AVAILABLE_TEXT
                    items_text += PRICE_ITEM_TEXT % {'part_number': mdv2_escape(search_item['part_number']),
                                                     'name': mdv2_escape(search_item['name']),
                                                     'available_text': available_text}

                    result_message_text += ''.join((items_text, '\n'))

                    search_item_count += 1
                    if search_item_count == MAX_FOUND_SEARCH_COUNT:
                        result_search_count = len(result_search_list)
                        result_message_text += MAX_FOUND_SEARCH_TEXT % str(result_search_count - MAX_FOUND_SEARCH_COUNT)

                        break

                result_message_text = result_message_text.rstrip()

        search_logging().info(SEARCH_LOG_SEPARATOR.join(('<', str(result_search_count))))
        await message.answer(result_message_text, parse_mode=ParseMode.MARKDOWN_V2)


def register_handlers(dp: Dispatcher):
    dp.message.register(txt_search, filter_chat_type_private, filter_content_type_text)
