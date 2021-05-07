import settings
from typing import List
import re
import json
import requests
from bs4 import BeautifulSoup


class AnimeScraper:
    def __init__(self, url: str):
        """
        Constructor for AnimeScraper.
        Scrapes some information about anime, which is used later for further
        scraping and downloading.

        :param url: Anime URL
        """
        # Soup object for scraping
        anime_soup = BeautifulSoup(
            requests.get(url, headers=settings.REQUEST_HEADERS).text,
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

        # This dictionary will later contain episodes information as well
        self.dataDict = {
            "anime-title": re.sub(
                '[<>?":/|]',
                "",
                anime_soup.title.text.replace("at Gogoanime", "").replace("Watch ", "").strip(),
            ),
            "anime-url": url,
        }

        ajax_soup = BeautifulSoup(
            requests.get(ajax_url, headers=settings.REQUEST_HEADERS).text,
            "html.parser",
        )
        self.episode_count = len(ajax_soup.find_all("a"))

        # Collect information of all episodes for further scraping later
        self.dataDict["episodes"] = []
        for li in reversed(ajax_soup.find_all("li")):
            episode_dict = {
                "episode-title": re.sub(
                    '[<>?":/|]',
                    "",
                    "{} - {}".format(self.dataDict["anime-title"], " ".join(li.text.split())),
                ),
                "episode-url": "https://www.gogoanime.so{}".format(li.find("a")["href"].strip()),
            }
            self.dataDict["episodes"].append(episode_dict)

    def scrape_episodes(self, start: int, end: int):
        """
        Scrapes episode data including embed video server URLs and store in the anime
        dictionary.

        :param start: Episode number to start from
        :param end: Episode number to end at
        """
        self.dataDict["scraped-episodes"] = []
        for episode_dict in self.dataDict["episodes"][start - 1 : end]:
            scraped_episode_dict = episode_dict
            soup = BeautifulSoup(
                requests.get(
                    episode_dict["episode-url"], headers=settings.REQUEST_HEADERS
                ).text,
                "html.parser",
            )
            servers_list = soup.find("div", {"class": "anime_muti_link"}).find_all("li")[1:]
            scraped_episode_dict["embed-servers"] = {}
            for li in servers_list:
                embed_url = li.find("a")["data-video"]

                # Sometimes, the "https:" part is excluded from URL
                if "https:" not in embed_url:
                    embed_url = f"https:{embed_url}"

                scraped_episode_dict["embed-servers"][li["class"][0]] = embed_url

            self.dataDict["scraped-episodes"].append(scraped_episode_dict)
            print("- Collected:", scraped_episode_dict["episode-title"])

    def save_json(self, filename: str):
        """
        Saves anime data in a JSON file, from the dictionary object.

        :param filename: Name for the file to be saved
        """
        open(filename, "w", encoding="utf-8").write(
            json.dumps(self.dataDict, indent=4, sort_keys=True, ensure_ascii=False)
        )

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
            BeautifulSoup(response_text, "html.parser")
            .find("ul", class_="items")
            .find_all("p", class_="name")[:4]
        )

        paired_results = [
            (
                p.find("a")["title"],
                "https://www.gogoanime.so{}".format(p.find("a")["href"]),
            )
            for p in p_results
        ]

        return paired_results


if __name__ == "__main__":
    anime_scraper = AnimeScraper(input("Enter Anime URL: "))
    anime_scraper.scrape_episodes(start=1, end=1)
    anime_scraper.save_json(filename="anime.json")
    print("- Saved JSON file!")
