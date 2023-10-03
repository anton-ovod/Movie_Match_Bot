from aiogram import Bot

from bot import redis_instance


async def set_data(data: dict, bot: Bot):
    await redis_instance.append("data", data)
