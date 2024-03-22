import aiohttp
import logging

from config_reader import config
from models.common import Rating

from models.detailedmovie import DetailedMovie
from models.detailedtvshow import DetailedTVShow
from models.detailedperson import DetailedPerson


async def get_subject_details_omdb(subject: DetailedMovie | DetailedTVShow | DetailedPerson) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            subject_details_url = config.omdb_base_url.get_secret_value()
            params = {
                "apikey": config.omdb_api_key.get_secret_value(),
                "i": subject.imdb_id,
            }
            async with session.get(subject_details_url, params=params) as response:
                subject_detail = await response.json()
                if countries := subject_detail.get("Country"):
                    subject.countries = countries.split(", ")
                if age_categories := subject_detail.get("Rated"):
                    if age_categories != "N/A":
                        subject.age_categories = age_categories
                if awards := subject_detail.get("Awards"):
                    if awards != "N/A":
                        subject.awards = awards
                if ratings := subject_detail.get("Ratings"):
                    for rating in ratings[1:]:
                        subject.ratings.append(Rating(source=rating.get("Source"), value=int(rating.get("Value")[0:2])))
                if imdb_rating := subject_detail.get("imdbRating"):
                    subject.ratings.append(Rating(source="IMDB", value=float(imdb_rating)))
    except Exception as e:
        logging.error(f"[OMDB API] Error while getting subject's details: {e}")
