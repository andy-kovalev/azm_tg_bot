from aiogram import types, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from bot.common_search import search
from bot.const.const_message import NOT_FOUND_SEARCH_TEXT, MAX_FOUND_SEARCH_COUNT, MAX_FOUND_SEARCH_TEXT, \
    AVAILABLE_TEXT, NOT_AVAILABLE_TEXT, PRICE_ITEM_TEXT
from bot.message_filters import filter_chat_type_private, filter_content_type_text
from bot.utils.text import mdv2_escape


async def txt_search(message: types.Message, state: FSMContext):
    result_message_text = NOT_FOUND_SEARCH_TEXT
    search_text = message.text
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
                    result_message_text += MAX_FOUND_SEARCH_TEXT % str(len(result_search_list) - MAX_FOUND_SEARCH_COUNT)
                    break

            result_message_text = result_message_text.rstrip()

    await message.answer(result_message_text, parse_mode=ParseMode.MARKDOWN_V2)


def register_handlers(dp: Dispatcher):
    dp.message.register(txt_search, filter_chat_type_private, filter_content_type_text)
