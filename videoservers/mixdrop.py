import settings
import models as mdl
import requests
import re


def get_download_link(ep: mdl.Episode) -> str:
    """
    Generates a download link for mixdrop embed video server

    :param ep: Episode model object
    :return: Download link of video from mixdrop
    """
    embed_url = ep.video_data.get("mixdrop")
    if not embed_url:
        return None

    try:
        response = requests.get(embed_url, headers=settings.REQUEST_HEADERS)

        # Return None if video server is not available
        if "tb error" in response.text:
            return None

        video_details = re.findall("MDCore\|\|.+\|poster", response.text)[0].split("|")
        # Example:
        # //s-delivery14.mxdcontent.net/v/59f0fcbf63176bff9792eb2b2c5218dd.mp4?
        # s=dZk3d430Oi1bSCD5HfvMbA&e=1616377672&_t=1616359487
        download_link = "https://{2}-{3}.{6}.{7}/v/{4}.{5}?{2}={9}&e={17}&{16}={18}".format(
            *video_details
        )
    except Exception as e:
        print(e)
        return None

    return download_link


if __name__ == "__main__":
    # Example: https://mixdrop.co/e/7rgov1qpuk4rq7
    epis = mdl.Episode(
        title="Test episode",
        url="Test URL",
        video_data={"embed-servers": {"mixdrop": input("Enter mixdrop embed URL: ")}}
    )
    print(get_download_link(epis))
