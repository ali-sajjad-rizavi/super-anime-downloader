from bs4 import BeautifulSoup
import requests
import re

my_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.116 Safari/537.36"
}


def get_download_link(ep: dict) -> str:
    """
    Generates a download link for mp4upload embed video server

    :param ep: Episode dictionary
    :return: Download link of video from mp4upload
    """
    # The class name for mp4upload server is either "mp4upload" or "mp4"
    embed_url = ep["embed-servers"].get("mp4upload", ep["embed-servers"].get("mp4"))
    if not embed_url:
        return None

    try:
        response = requests.get(embed_url, headers=my_headers)

        scripts = BeautifulSoup(response.text, "html.parser").find_all(
            "script", type="text/javascript"
        )
        eval_text = [str(script) for script in scripts if "|embed|" in str(script)][0]
        eval_items = eval_text.split("|")
        del eval_items[: eval_items.index("mp4upload") + 1]
        video_id = [a for a in eval_items if len(a) > 30][0]
        eval_items = eval_text.split("|")

        w3str_possibles_list = [
            s for s in eval_items if re.match("s\d+$", s) or re.match("www\d+$", s)
        ]
        w3str = "www"
        if len(w3str_possibles_list) != 0:
            w3str = max(w3str_possibles_list, key=len)

        download_link = "https://{}.mp4upload.com:{}/d/{}/video.mp4".format(
            w3str, eval_items[eval_items.index(video_id) + 1], video_id
        )
    except Exception as e:
        print(e)
        return None

    return download_link


# A sample Mp4Upload embedded URL: https://www.mp4upload.com/embed-99r0hr81zk9k.html
if __name__ == "__main__":
    print("\t\t=====================")
    print("\t\t Mp4Upload Generator")
    print("\t\t=====================")
    try:
        d = get_download_link(
            {"embed-servers": {"mp4upload": input("\t- Enter Mp4Upload Embed URL: ")}}
        )
        print(f"- The generated download link: {d}")
    except Exception as e:
        print("\tSomething went wrong while generating the Download link!")
        print("Error message: ", e)
