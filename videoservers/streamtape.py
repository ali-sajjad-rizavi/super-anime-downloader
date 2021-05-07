import settings
from bs4 import BeautifulSoup
import requests


def get_download_link(ep: dict) -> str:
    """
    Generates a download link for streamtape embed video server

    :param ep: Episode dictionary
    :return: Download link of video from streamtape
    """
    embed_url = ep["embed-servers"].get("streamtape")
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
    print(
        get_download_link({"embed-servers": {"streamtape": input("Enter streamtape embed URL: ")}})
    )
