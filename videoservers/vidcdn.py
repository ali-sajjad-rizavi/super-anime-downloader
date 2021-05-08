import settings
import models as mdl
import requests
from bs4 import BeautifulSoup
import re


def get_download_link(ep: mdl.Episode) -> str:
    """
    Generates a download link for vidcdn embed video server

    :param ep: Episode model object
    :return: Download link of video
    """
    embed_url = ep.video_data.get("vidcdn")
    if not embed_url:
        return None

    try:
        soup = BeautifulSoup(
            requests.get(embed_url, headers=settings.REQUEST_HEADERS).text, "html.parser"
        )
        js_text = str(soup.find("div", class_="videocontent"))
        download_link = re.findall("file: '(.+?)'", js_text)[0]
    except Exception as e:
        print(e)
        return None

    return download_link


# Example: https://vidstreaming.io/load.php?id=OTc2MzI=&title=Boruto%3A+Naruto+Next+Generations+Episode+1
if __name__ == "__main__":
    epis = mdl.Episode(
        title="Test title",
        url="Test URL",
        video_data={"embed-servers": {"vidcdn": input("Enter vidcdn embed URL: ")}}
    )
    print(get_download_link(epis))
