import logging
import asyncio
import sys

from redis.asyncio.client import Redis

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from aiogram_dialog import setup_dialogs

from handlers.home_dialog import home_router
from handlers.searching.movie_dialog import movie_search_router

from config_reader import config


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    storage = RedisStorage(Redis(),
                           key_builder=DefaultKeyBuilder(with_destiny=True))

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=storage)

    dp.include_routers(movie_search_router, home_router)

    setup_dialogs(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logging.critical(e)


