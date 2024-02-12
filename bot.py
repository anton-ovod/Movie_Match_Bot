import logging
import asyncio
import sys

from utils.caching_handlers import redis_instance

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder, RedisEventIsolation

from aiogram_dialog import setup_dialogs

from handlers.home_dialog import home_router
from handlers.searching.movie_dialog import movie_search_router

from dialogs.home_dialog import home_dialog
from dialogs.searching.movie_dialog import movie_dialog

from config_reader import config


storage = RedisStorage(redis_instance,
                       key_builder=DefaultKeyBuilder(with_destiny=True))

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=storage,
                event_isolation=RedisEventIsolation(redis=storage.redis))


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    home_router.include_router(home_dialog)
    movie_search_router.include_router(movie_dialog)

    dp.include_routers(home_router, movie_search_router)
    setup_dialogs(dp)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logging.critical(e)
