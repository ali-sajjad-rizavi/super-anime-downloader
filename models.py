from dataclasses import dataclass
from typing import List


@dataclass
class Episode:
    """Model for an episode of anime"""

    title: str
    url: str

    # Contains embed server video urls
    video_data: dict = None


@dataclass
class Anime:
    """Model for anime"""

    title: str
    url: str
    episodes: List[Episode] = None
