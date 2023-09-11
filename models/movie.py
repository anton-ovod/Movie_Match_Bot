import aiohttp
import logging

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
    def __init__(self, tmdb_id: int):
        self._tmdb_id: int = tmdb_id
        self._imdb_id: str = ""
        self._title: str = ""
        self._release_date: str = ""
        self._overview: str = ""
        self._tagline: str = ""
        self._genres: List[str] = []
        self._runtime: str = ""
        self._ratings: List[Dict[str, str]] = [
            {
                "source": "IMDB",
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
                "source": "TMDb",
                "value": "-"
            }
        ]
        self._poster_url: str = ""
        self._trailer_url: str = ""
        self._cast: List[Dict[str, str]] = []
        self._homepage: str = ""
        self._awards: str = ""
        self._country: str = ""
        self._year_categories: List[str] = []

    @property
    def homepage(self):
        return self._homepage

    @property
    def poster_url(self):
        return self._poster_url

    @property
    def imdb_url(self):
        if self._imdb_id:
            return self._create_link_to_imdb()
        return ""

    @property
    def trailer_url(self):
        return self._trailer_url

    @property
    def tmdb_url(self):
        return self._create_link_to_tmdb()

    @property
    def title_year(self):
        return self._title + " " + self._release_date[:4] if self._release_date else self._title

    async def _get_movie_details_tmdb(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = f"{config.movie_details_url.get_secret_value()}/{self._tmdb_id}"
                params = {
                    "api_key": config.api_key.get_secret_value(),
                    "language": "en-US",
                    "append_to_response": "credits,videos",
                }
                async with session.get(movie_details_url, params=params) as response:
                    movie_detail = await response.json()
                    self._title = movie_detail.get("title")
                    self._release_date = movie_detail.get("release_date")
                    if movie_detail.get("tagline"):
                        self._tagline = movie_detail.get("tagline")
                    if movie_detail.get("genres", []):
                        self._genres = [genre.get("name") for genre in movie_detail.get("genres")]
                    if movie_detail.get("homepage"):
                        self._homepage = movie_detail.get("homepage")
                    self._overview = movie_detail.get("overview")
                    if movie_detail.get("imdb_id") is not None:
                        self._imdb_id = str(movie_detail.get("imdb_id"))
                        await self._get_movie_details_omdb()
                    if movie_detail.get("poster_path"):
                        self._poster_url = (f"{config.base_image_url.get_secret_value()}"
                                            f"{movie_detail.get('poster_path')}")
                    if movie_detail.get("runtime") is not None:
                        self._runtime = str(movie_detail.get("runtime"))
                    if movie_detail.get("vote_average") is not None and movie_detail.get("vote_average") != 0:
                        self._ratings[3]["value"] = str(int(movie_detail.get("vote_average") * 10))

                    if movie_detail.get("videos", {}).get("results", []):
                        for video in movie_detail.get("videos", {}).get("results", []):
                            if video.get("type") == "Trailer":
                                self._trailer_url = f"{config.base_video_url.get_secret_value()}{video.get('key')}"
                                logging.info(f"Trailer url: {self._trailer_url}")
                                break

                    if movie_detail.get("credits", {}).get("cast", []):
                        for cast in movie_detail.get("credits", {}).get("cast", [])[:3]:
                            self._cast.append({
                                "name": cast.get("name"),
                                "character": cast.get("character")
                            })

        except Exception as e:
            logging.error(f"Error while getting movie details(TMDB): {e}")

    async def _get_movie_details_omdb(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = config.omdb_base_url.get_secret_value()
                logging.info("IMDB ID: " + self._imdb_id)
                params = {
                    "apikey": config.omdb_api_key.get_secret_value(),
                    "i": self._imdb_id,
                }
                async with session.get(movie_details_url, params=params) as response:
                    movie_detail = await response.json()
                    self._awards = movie_detail.get("Awards")

                    if movie_detail.get("Ratings", [])[1:]:
                        for rating in movie_detail.get("Ratings", [])[1:]:
                            if rating.get("Source", "") == "Rotten Tomatoes":
                                self._ratings[1]["value"] = rating.get("Value", "")[:2]
                            if rating.get("Source", "") == "Metacritic":
                                self._ratings[2]["value"] = rating.get("Value", "")[:2]
                    if movie_detail.get("imdbRating", "") != "N/A":
                        self._ratings[0]["value"] = movie_detail.get("imdbRating", "")

                    if movie_detail.get("Rated", ""):
                        for category in movie_detail.get("Rated", "").split(", "):
                            self._year_categories.append(category)

                    if movie_detail.get("Director", ""):
                        self._cast.append({
                            "name": movie_detail.get("Director"),
                            "character": "Director"
                        })
                    if movie_detail.get("Country") != "N/A":
                        self._country = movie_detail.get("Country")
        except Exception as e:
            logging.error(f"Error while getting movie details(OMDB): {e}")

    async def get_movie_details(self) -> None:
        await self._get_movie_details_tmdb()

    def _create_html_title_link(self) -> str:
        release_date = f" ({self._release_date[:4]})" if self._release_date else ""
        url = self._create_link_to_tmdb()
        if self._poster_url:
            url = self._poster_url
        elif self._imdb_id:
            url = self._create_link_to_imdb()
        return f"<b><a href = '{url}'>{self._title}{release_date}</a></b>\n"

    def _create_html_tagline(self) -> str:
        if self._tagline:
            return f"<i>{self._tagline}</i>\n\n"
        return "\n"

    def _create_html_genres(self) -> str:
        if self._genres:
            return " ".join([f"#{genre.replace(' ', '')} " for genre in self._genres]) + "\n"
        return ""

    def _create_html_overview(self) -> str:
        if self._overview:
            return f"{self._overview}\n\n"
        return ""

    def _calculate_average_rating(self) -> int | str:
        total_rating = 0
        total_count = 0

        for rating in self._ratings:
            value = rating.get("value")
            source = rating.get("source")
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
        ratings += (f"• <a href = '{self._create_link_to_imdb()}'>"
                    f"{self._ratings[0]['source']}</a>: {self._ratings[0]['value']}\n")
        ratings += (f"• <a href = '{self._create_link_to_rotten_tomatoes()}'>"
                    f"{self._ratings[1]['source']}</a>: {self._ratings[1]['value']}\n")
        ratings += (f"• <a href = '{self._create_link_to_metacritic()}'>"
                    f"{self._ratings[2]['source']}</a>: {self._ratings[2]['value']}\n")
        ratings += (f"• <a href = '{self._create_link_to_tmdb()}'>"
                    f"{self._ratings[3]['source']}</a>: {self._ratings[3]['value']}\n")
        return ratings + "\n"

    def _create_html_award(self) -> str:
        if self._awards != "N/A" and self._awards:
            return f"<b>Awards:</b> {self._awards}\n\n"
        else:
            return ""

    def _create_html_cast(self) -> str:
        cast = ""
        if self._cast:
            cast += f"<b>Director:</b> {self._cast[-1]['name']}\n\n"
            if len(self._cast) > 1:
                cast += "<b>Actors:</b>\n"
                for actor in self._cast[:-1]:
                    cast += f"<i>{actor['name']}</i> {' as ' + actor['character'] if actor['character'] else ''}\n"
                cast += "\n"

        return cast

    def _create_html_bottom_details(self) -> str:
        bottom_details = ""
        if self._year_categories and self._year_categories[0] != "N/A":
            bottom_details += f"{', '.join(self._year_categories)} | "
        if self._runtime:
            bottom_details += f"{self._runtime} min"
        if self._country:
            if self._runtime or self._year_categories:
                bottom_details += " | "
            bottom_details += f"{self._country}"
        return bottom_details

    def _create_link_to_tmdb(self):
        return f"https://www.themoviedb.org/movie/{self._tmdb_id}"

    def _create_link_to_imdb(self):
        return f"https://www.imdb.com/title/{self._imdb_id}"

    def _create_link_to_rotten_tomatoes(self):
        title = self._title.replace(' ', '_').replace(':', '_').lower().replace("'", '_')
        return f"https://www.rottentomatoes.com/m/{title}"

    def _create_link_to_metacritic(self):
        title = self._title.replace(' ', '-').replace(':', '-').lower().replace("'", '')
        return f"https://www.metacritic.com/movie/{title}"

    # creating a html based message with movie details
    def create_movie_message(self) -> str:
        message = ""
        message += self._create_html_title_link()
        message += self._create_html_tagline()
        message += self._create_html_genres()
        message += self._create_html_overview()
        message += self._create_html_movie_ratings()
        message += self._create_html_award()
        message += self._create_html_cast()
        message += self._create_html_bottom_details()
        return message
