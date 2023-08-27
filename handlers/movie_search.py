import aiohttp

from config_reader import config


async def get_movies_by_title(title: str):
    async with aiohttp.ClientSession() as session:
        search_movie_url = config.search_movie_url.get_secret_value()
        params = {
            "api_key": config.api_key.get_secret_value(),
            "query": title
        }
        async with session.get(search_movie_url, params=params) as response:
            return await response.json()
