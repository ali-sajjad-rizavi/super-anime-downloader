import settings
import models as mdl
from bs4 import BeautifulSoup
import requests


def get_download_link(ep: mdl.Episode) -> str:
    """
    Generates a download link for streamtape embed video server

    :param ep: Episode model object
    :return: Download link of video from streamtape
    """
    embed_url = ep.video_data.get("streamtape")
    if not embed_url:
        return None

    try:
        response = requests.get(embed_url, headers=settings.REQUEST_HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        text = [str(script) for script in soup.find_all("script") if ").innerHTML" in str(script)][
            0
        ]
        text = "".join(text.rstrip("</script>").lstrip("<script>").split())
        text = text.split("innerHTML=")[1].rstrip(";")
        text = "".join([substr.strip('"').strip("'") for substr in text.split("+")])

        download_link = f"https:{text}"
    except Exception as e:
        print(e)
        return None

    return download_link


if __name__ == "__main__":
    # Example: https://streamtape.com/e/YqKyKxg23jivJDB/world-trigger-2nd-season-episode-10.mp4
    epis = mdl.Episode(
        title="Test title",
        url="Test URL",
        video_data={"embed-servers": {"streamtape": input("Enter streamtape embed URL: ")}}
    )
    print(get_download_link(epis))
