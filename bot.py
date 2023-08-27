import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import common_commands, search, back_handler

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp = Dispatcher()
    dp.include_routers(common_commands.router, search.router, back_handler.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
