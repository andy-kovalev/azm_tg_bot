from bot.utils.text import _B, _E, mdv2_escape

HELP_TEXT = '''Я бот <b>Капот</b>, помощник в проверке наличия запасных частей Caterpillar и MWM

Я помогу тебе узнать наличие запасных частей и подскажу контакты компании Azimut для их покупки или заказа

Напиши мне каталожный номер или название запасной части и я проверю наличие на складе
'''

START_TEXT = '''<b>Привет!</b>
''' + HELP_TEXT

NOT_FOUND_SEARCH_TEXT = mdv2_escape('''К сожалению, я не нашел ничего по Вашему запросу

Попробуйте изменить запрос, чтобы я мог найти товар в каталоге или обратитесь к менеджеру
+7(952)201-00-63, +7(921)318-36-00
office@azimut.llc
''')
AVAILABLE_TEXT = f'{_B}В наличии{_B}'

NOT_AVAILABLE_TEXT = 'Нет в наличии'

PRICE_ITEM_TEXT = f'''{_B}%(part_number)s{_B} %(name)s
%(available_text)s
'''

# ограничение Telegram на длину сообщения
MAX_MESSAGE_SYMBOL_LENGTH = 9500

MAX_FOUND_SEARCH_COUNT = 10

MAX_FOUND_SEARCH_TEXT = (f'{_B}Ещё{_B} найдено {_B}%s товаров{_B} в каталоге, уточните поиск {_E}.{_E}.{_E}.')

UPLOAD_FILE_SUCCESS_TEXT = 'Файл успешно загружен и используется для поиска наличия запасных частей'

UPLOAD_FILE_ERROR_TEXT = 'Ошибка загрузки файла, обратитесь к разработчику сервиса'
