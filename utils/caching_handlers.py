import logging
from typing import Union, List
from datetime import timedelta
from redis.asyncio.client import Redis


redis_instance = Redis(decode_responses=True)


async def set_data(redis_key: str, data: list[str] | str) -> None:
    """
    Set data to Redis.

    :param redis_key:  The Redis key to set data to.
    :param data:  The data to set.
    :return:  None

    """
    try:
        if isinstance(data, list):
            await redis_instance.rpush(redis_key, *data)
            await redis_instance.expire(redis_key, timedelta(hours=12))
        else:
            await redis_instance.set(redis_key, data)
            await redis_instance.expire(redis_key, timedelta(hours=12))
    except Exception as e:
        logging.error(f"Error setting data to Redis: {str(e)}")


async def is_exist(key: str) -> bool:
    """
    Check if key exists in Redis.

    :param key:  The Redis key to check.
    :return:  True if key exists, False otherwise.

    """
    try:
        return await redis_instance.exists(key)
    except Exception as e:
        logging.error(f"Error checking if key exists in Redis: {str(e)}")
        return False


async def get_data(key: str) -> Union[str, int, List[str]]:
    """
    Get data from Redis.

    :param key:  The Redis key to get data from.
    :return:  The data from Redis.

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
