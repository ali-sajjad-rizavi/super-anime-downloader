import requests
from bs4 import BeautifulSoup
import re

my_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.116 Safari/537.36"
}


def get_download_link(ep: dict) -> str:
    """
    Generates a download link for vidcdn embed video server

    :param ep: Episode dictionary
    :return: Download link of video
    """
    embed_url = ep["embed-servers"].get("vidcdn")
    if not embed_url:
        return None

    try:
        soup = BeautifulSoup(requests.get(embed_url, headers=my_headers).text, "html.parser")
        js_text = str(soup.find("div", class_="videocontent"))
        download_link = re.findall("file: '(.+?)'", js_text)[0]
    except Exception as e:
        print(e)
        return None

    return download_link


# Example: https://vidstreaming.io/load.php?id=OTc2MzI=&title=Boruto%3A+Naruto+Next+Generations+Episode+1
if __name__ == "__main__":
    print(get_download_link({"embed-servers": {"vidcdn": input("Enter vidcdn embed URL: ")}}))
