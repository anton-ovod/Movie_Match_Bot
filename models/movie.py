import aiohttp
import logging

from aiogram.utils.markdown import hide_link, bold, italic

from typing import Dict, List

from config_reader import config


class KeyboardMovie:
    def __init__(self, title, release_date, tmdb_id):
        self._title: str = title
        self._year: str = release_date[:4]
        self._tmdb_id: str = tmdb_id

    def __repr__(self):
        return f"Keyboard Movie: {self.title} : {self._tmdb_id}"

    @property
    def title(self) -> str:
        return f"{self._title} ({self._year})" if self._year else f"{self._title}"

    @property
    def get_main_data(self) -> Dict[str, str]:
        return {
            "title": self._title,
            "release_date": self._year,
            "tmdb_id": self._tmdb_id
        }


class Movie:
    def __init__(self, tmdb_id):
        self.tmdb_id: int = tmdb_id
        self.imdb_id: str = ""
        self.title: str = ""
        self.release_date: str = ""
        self.overview: str = ""
        self.tagline: str = ""
        self.genres: List[str] = []
        self.runtime: str = ""
        self.ratings: List[Dict[str, str]] = [
            {
                "source": "TMDB",
                "value": "-"
            },
            {
                "source": "Rotten Tomatoes",
                "value": "-"
            },
            {
                "source": "Metacritic",
                "value": "-"
            },
            {
                "source": "IMDB",
                "value": "-"
            }
        ]
        self.poster_url: str = ""
        self.trailer_url: str = ""
        self.cast: List[Dict[str, str]] = []
        self.homepage: str = ""
        self.awards: str = ""
        self.country: str = ""
        self.year_categories: List[str] = []

    async def _get_movie_details_tmdb(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = f"{config.movie_details_url.get_secret_value()}/{self.tmdb_id}"
                params = {
                    "api_key": config.api_key.get_secret_value(),
                    "language": "en-US",
                    "append_to_response": "credits,videos",
                }
                async with session.get(movie_details_url, params=params) as response:
                    movie_detail = await response.json()
                    logging.info(movie_detail)
                    self.title = movie_detail.get("title")
                    self.release_date = movie_detail.get("release_date")
                    if movie_detail.get("tagline"):
                        self.tagline = movie_detail.get("tagline")
                    if movie_detail.get("genres", []):
                        self.genres = [genre.get("name") for genre in movie_detail.get("genres")]
                    if movie_detail.get("homepage"):
                        self.homepage = movie_detail.get("homepage")
                    self.overview = movie_detail.get("overview")
                    if movie_detail.get("imdb_id") is not None:
                        self.imdb_id = str(movie_detail.get("imdb_id"))
                    if movie_detail.get("poster_path"):
                        self.poster_url = f"{config.base_image_url.get_secret_value()}{movie_detail.get('poster_path')}"
                    if movie_detail.get("runtime") is not None:
                        self.runtime = str(movie_detail.get("runtime"))
                    if movie_detail.get("vote_average") is not None and movie_detail.get("vote_average") != 0:
                        self.ratings[0]["value"] = str(int(movie_detail.get("vote_average", None) * 10))

                    if movie_detail.get("videos", {}).get("results", []):
                        for video in movie_detail.get("videos", {}).get("results", []):
                            if video.get("type", "") == "Trailer":
                                self.trailer_url = f"{config.base_video_url}{video.get('key')}"
                                break

                    if movie_detail.get("credits", {}).get("cast", []):
                        for cast in movie_detail.get("credits", {}).get("cast", [])[:3]:
                            self.cast.append({
                                "name": cast.get("name"),
                                "character": cast.get("character")
                            })

        except Exception as e:
            logging.error(f"Error while getting movie details(TMDB): {e}")

    async def _get_movie_details_omdb(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = config.omdb_base_url.get_secret_value()
                logging.info("IMDB ID: " + self.imdb_id)
                params = {
                    "apikey": config.omdb_api_key.get_secret_value(),
                    "i": self.imdb_id,
                }
                async with session.get(movie_details_url, params=params) as response:
                    movie_detail = await response.json()
                    logging.info(movie_detail)
                    self.awards = movie_detail.get("Awards")

                    if movie_detail.get("Ratings", [])[1:]:
                        for rating in movie_detail.get("Ratings", [])[1:]:
                            if rating.get("Source", "") == "Rotten Tomatoes":
                                self.ratings[1]["value"] = rating.get("Value", "")[:2]
                            if rating.get("Source", "") == "Metacritic":
                                self.ratings[2]["value"] = rating.get("Value", "")[:2]
                    if movie_detail.get("imdbRating", "") != "N/A":
                        self.ratings[3]["value"] = movie_detail.get("imdbRating", "")

                    if movie_detail.get("Rated", ""):
                        for category in movie_detail.get("Rated", "").split(", "):
                            self.year_categories.append(category)

                    if movie_detail.get("Director", ""):
                        self.cast.append({
                            "name": movie_detail.get("Director"),
                            "character": "Director"
                        })
                    if movie_detail.get("Country") != "N/A":
                        self.country = movie_detail.get("Country")
        except Exception as e:
            logging.error(f"Error while getting movie details(OMDB): {e}")

    async def get_movie_details(self) -> None:
        await self._get_movie_details_tmdb()
        if self.imdb_id:
            await self._get_movie_details_omdb()

    def _create_html_title_link(self) -> str:
        return f"<b><a href = '{self.poster_url}'>{self.title + ' (' + self.release_date[:4] + ')' if self.release_date else self.title}</a></b>"

    def _create_html_tagline(self) -> str:
        return f"<i>{self.tagline}</i>"

    def _create_html_genres(self) -> str:
        return " ".join([f"#{genre.replace(' ', '')} " for genre in self.genres])

    def _create_html_overview(self) -> str:
        return f"{self.overview}"

    def _calculate_average_rating(self) -> int | str:
        total_rating = 0
        total_count = 0

        for rating in self.ratings:
            value = rating["value"]
            source = rating["source"]
            # Extract numerical value from the rating string
            try:
                if source == "IMDB":
                    value = float(value.split("/")[0]) * 10
                rating_value = float(value)
                total_rating += rating_value
                total_count += 1
            except ValueError:
                continue

        if total_count == 0:
            return "-"

        average_rating = total_rating // total_count
        return int(average_rating)

    def _create_html_movie_ratings(self) -> str:
        star_characters = {
            0: "🌑🌑🌑🌑🌑",
            0.5: "🌗🌑🌑🌑🌑",
            1: "🌕🌑🌑🌑🌑",
            1.5: "🌕🌗🌑🌑🌑",
            2: "🌕🌕🌑🌑🌑",
            2.5: "🌕🌕🌗🌑🌑",
            3: "🌕🌕🌕🌑🌑",
            3.5: "🌕🌕🌕🌗🌑",
            4: "🌕🌕🌕🌕🌑",
            4.5: "🌕🌕🌕🌕🌗",
            5: "🌕🌕🌕🌕🌕"
        }
        average_rating = self._calculate_average_rating()
        try:
            star_rating = star_characters[round((average_rating / 20) * 2) / 2]
        except (TypeError, KeyError):
            star_rating = star_characters[0]

        ratings = ""
        ratings += f"<b>Average rating: {star_rating} • {average_rating}</b>\n"
        ratings += f"• <a href = '{self._create_link_to_tmdb()}'>{self.ratings[0]['source']}</a>: {self.ratings[0]['value']}\n"
        ratings += f"• <a href = '{self._create_link_to_rotten_tomatoes()}'>{self.ratings[1]['source']}</a>: {self.ratings[1]['value']}\n"
        ratings += f"• <a href = '{self._create_link_to_metacritic()}'>{self.ratings[2]['source']}</a>: {self.ratings[2]['value']}\n"
        ratings += f"• <a href = '{self._create_link_to_imdb()}'>{self.ratings[3]['source']}</a>: {self.ratings[3]['value']}\n"
        return ratings

    def _create_html_award(self) -> str:
        if self.awards != "N/A" and self.awards:
            return f"<b>Awards:</b> {self.awards}\n\n"
        else:
            return ""

    def _create_html_cast(self) -> str:
        cast = ""
        if self.cast:
            cast += f"<b>Director:</b> {self.cast[-1]['name']}\n\n"
            cast += "<b>Actors:</b>\n"
            for actor in self.cast[:-1]:
                cast += f"<i>{actor['name']}</i> {' as ' + actor['character'] if actor['character'] else ''}\n"

        return cast

    def _create_html_bottom_details(self) -> str:
        bottom_details = ""
        if self.year_categories:
            bottom_details += f"{', '.join(self.year_categories)} | "
        if self.runtime:
            bottom_details += f"{self.runtime} min | "
        if self.country:
            bottom_details += f"{self.country}"
        return bottom_details

    def _create_link_to_tmdb(self):
        return f"https://www.themoviedb.org/movie/{self.tmdb_id}"

    def _create_link_to_imdb(self):
        return f"https://www.imdb.com/title/{self.imdb_id}"

    def _create_link_to_rotten_tomatoes(self):
        title = self.title.replace(' ', '_').replace(':', '_').lower().replace("'", '_')
        return f"https://www.rottentomatoes.com/m/{title}"

    def _create_link_to_metacritic(self):
        title = self.title.replace(' ', '-').replace(':', '-').lower().replace("'", '')
        return f"https://www.metacritic.com/movie/{title}"

    # creating a html based message with movie details
    def create_movie_message(self) -> str:
        message = ""
        message += self._create_html_title_link() + "\n"
        message += self._create_html_tagline() + "\n\n"
        message += self._create_html_genres() + "\n"
        message += self._create_html_overview() + "\n\n"
        message += self._create_html_movie_ratings() + "\n"
        message += self._create_html_award()
        message += self._create_html_cast() + "\n"
        message += self._create_html_bottom_details()
        return message
