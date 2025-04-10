import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage

import settings

try:
    bot = Bot(token=settings.BOT_TOKEN)
    logging.debug(f'bot: Create bot with token={settings.BOT_TOKEN_OBFUSCATED}')
except Exception as err:
    bot = None
    logging.critical(f'bot: Can\'t create bot! [{err}]', )

# if len(settings.FSM_REDIS_STORAGE_ADDRESS) > 0:
#     try:
#         storage = RedisStorage.from_url(settings.FSM_REDIS_STORAGE_URL)
#         logging.debug('bot: Use RedisStorage for FSMContext')
#     except Exception as err:
#         storage = None
#         bot = None
#         logging.critical(f'bot: Can\'t create RedisStorage [{err}]')
# else:
storage = MemoryStorage()
logging.debug('bot: Use MemoryStorage for FSMContext')

try:
    dp = Dispatcher(storage=storage)
    logging.debug('bot: Create Dispatcher')
except Exception as err:
    dp = None
    logging.critical(f'bot: Can\'t create bot dispatcher! [{err}]')
