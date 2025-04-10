# """
# Telegram Bot
# Для проверки наличия запасных частей, bot providing interface for azimut common search
# """
from asyncio import run

from bot import handlers
from bot.bot import bot, dp


async def start_bot_service():
    await dp.start_polling(bot)


if __name__ == '__main__':
    handlers.register_handlers(dp)
    run(start_bot_service(), debug=True)
