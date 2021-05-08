import settings
import models as mdl
from typing import List
import re
import json
import requests
from bs4 import BeautifulSoup


class AnimeScraper:
    def __init__(self, anime_url: str):
        """
        Constructor for AnimeScraper.
        Scrapes some information about anime, which is used later for further
        scraping and downloading.

        :param anime_url: Anime URL
        """
        # Soup object for scraping
        anime_soup = BeautifulSoup(
            requests.get(anime_url, headers=settings.REQUEST_HEADERS).text,
            "html.parser",
        )

        # GET request parameters for ajax URL
        id_ = anime_soup.find(id="movie_id")["value"]
        alias = anime_soup.find(id="alias_anime")["value"]
        last_ep = anime_soup.find(id="episode_page").find_all("a")[-1]["ep_end"]

        # We collect the list of all episodes and their links using this URL
        ajax_url = (
            "https://ajax.gogocdn.net/ajax/load-list-episode?ep_start=0&default_ep=0"
            f"&ep_end={last_ep}&id={id_}&alias={alias}"
        )

        # Remove bad characters from anime title
        t = anime_soup.title.text.replace("at Gogoanime", "").replace("Watch ", "").strip()
        t = re.sub('[<>?":/|]', "", t)
        # Model object for anime. Episodes will be scraped and added to it
        self.anime = mdl.Anime(title=t, url=anime_url, episodes=[])

        ajax_soup = BeautifulSoup(
            requests.get(ajax_url, headers=settings.REQUEST_HEADERS).text,
            "html.parser",
        )

        # Collect information of all episodes for further scraping later
        for li in reversed(ajax_soup.find_all("li")):
            # Remove bad characters from scarped episode title
            ep_title = re.sub('[<>?":/|]', "", " ".join(li.text.split()))

            # Episode model object. Video data attribute will be set after scraping
            # the specified range of episodes.
            ep = mdl.Episode(
                title=f"{self.anime.title} - {ep_title}",
                url="https://www.gogoanime.so{}".format(li.find("a")["href"].strip())
            )

            # Append to list of episodes in anime model object
            self.anime.episodes.append(ep)

    def scrape_episodes(self, start: int, end: int):
        """
        Scrapes episode data including embed video server URLs and store in
        the episodes model objects present in anime model object.

        :param start: Episode number to start from
        :param end: Episode number to end at
        """
        for ep in self.anime.episodes[start - 1: end]:
            soup = BeautifulSoup(
                requests.get(ep.url, headers=settings.REQUEST_HEADERS).text,
                "html.parser",
            )
            servers_list = soup.find("div", {"class": "anime_muti_link"}).find_all("li")[1:]

            # Data of embed servers will be collected in video_data attribute
            ep.video_data = {}

            for li in servers_list:
                embed_url = li.find("a")["data-video"]

                # Sometimes, the "https:" part is excluded from URL
                if "https:" not in embed_url:
                    embed_url = f"https:{embed_url}"

                # Collect embed urls into the dictionary
                ep.video_data[li["class"][0]] = embed_url

            print(f"- Collected: {ep.title}")

    @staticmethod
    def search_anime(q: str) -> List[tuple]:
        """
        Searches anime from website using the given keyword

        :param q: Anime name to search
        :return: List of tuples containing title of anime and it's URL
        """
        response_text = requests.get(
            "https://www.gogoanime.so/search.html?keyword={}".format(q.replace(" ", "%20"))
        ).text

        p_results = (
            BeautifulSoup(response_text, "html.parser").find("ul", class_="items").find_all("p", class_="name")[:4]
        )

        paired_results = [
            (
                p.find("a")["title"],
                "https://www.gogoanime.so{}".format(p.find("a")["href"]),
            )
            for p in p_results
        ]

        return paired_results
