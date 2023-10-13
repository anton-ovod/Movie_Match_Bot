import json
import logging
from typing import Union, List
from datetime import timedelta
from redis.asyncio.client import Redis

from models.movie import KeyboardMovie

from misc.serialization import serialize_datetime

redis_instance = Redis(decode_responses=True)


async def set_data(redis_key: str, data: list[str] | str) -> None:
    try:
        if isinstance(data, list):
            await redis_instance.rpush(redis_key, *data)
            await redis_instance.expire(redis_key, timedelta(hours=12))
        else:
            await redis_instance.set("data", data)
            await redis_instance.expire(redis_key, timedelta(hours=12))
    except Exception as e:
        logging.error(f"Error setting data to Redis: {str(e)}")



async def is_exist(key: str) -> bool:
    """
    Check if key exists in Redis.

    Args:
        key (str): The Redis key to check.

    Returns:
        bool: True if key exists, False otherwise.
    """
    try:
        return await redis_instance.exists(key)
    except Exception as e:
        logging.error(f"Error checking if key exists in Redis: {str(e)}")
        return False


async def get_data(key: str) -> Union[str, int, List[KeyboardMovie]]:
    """
    Retrieve data from Redis by key.

    Args:
        key (str): The Redis key to retrieve data from.

    Returns:
        Union[str, int, List[KeyboardMovie]]: The retrieved data or 0 if not found.
    """
    try:
        if await redis_instance.type(key) == 'list':
            data = await redis_instance.lrange(key, 0, -1)
            return data
        else:
            result = await redis_instance.get(key)
        return result
    except Exception as e:
        logging.error(f"Error retrieving data from Redis: {str(e)}")
