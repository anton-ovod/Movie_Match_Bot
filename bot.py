import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import common_commands, movie_search

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp = Dispatcher()
    dp.include_routers(common_commands.router, movie_search.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
