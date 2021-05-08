from dataclasses import dataclass
from typing import List


@dataclass
class Episode:
    """Model for an episode of anime"""

    title: str
    url: str

    # Contains embed server video urls
    video_data: dict = None

    # A fresh generated download link will be set in this attribute
    download_link: str = None


@dataclass
class Anime:
    """Model for anime"""

    title: str
    url: str
    episodes: List[Episode] = None

    def get_scraped_episodes(self) -> List[Episode]:
        """
        Returns the list of episodes which were scraped.

        :return: List of Episode model objects
        """
        return [ep for ep in self.episodes if ep.video_data]
