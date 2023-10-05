import json
import logging
from typing import Any

from redis.asyncio.client import Redis

from models.movie import KeyboardMovie

redis_instance = Redis()


async def set_data(redis_key: str, data: list[KeyboardMovie] | str) -> None:
    if isinstance(data, list):
        await redis_instance.rpush(redis_key, *[item.model_dump_json() for item in data])
    else:
        await redis_instance.set("data", data)


async def get_data(key: str) -> str | int | list[KeyboardMovie] | Any:
    if await redis_instance.exists(key):
        if await redis_instance.type(key) == "list":
            data = await redis_instance.lrange(key, 0, -1)
            logging.info(f"Data from redis: {data}")
            result = [KeyboardMovie(**json.loads(item)) for item in data]
            return result
        else:
            result = await redis_instance.get(key)
        return result
    return 0
