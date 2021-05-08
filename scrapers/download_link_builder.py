import models as mdl
import videoservers.mp4upload
import videoservers.vidcdn
import videoservers.mixdrop
import videoservers.streamtape


def get_available_download_link(ep: mdl.Episode) -> str:
    """
    Finds the best available download link using episode information provided
    in given dictionary.

    :param ep: Episode dictionary
    :return: Best available video download URL
    """
    if not ep.video_data:
        msg = f"The episode '{ep.title}' has no video_data"
        raise Exception(msg)

    # This list is ordered by the most preferred video server at top, and least
    # preferred at the end. We can easily prioritize our preferred video server
    # by rearranging the functions in this list.
    download_link_functions = [
        videoservers.mixdrop.get_download_link,
        videoservers.streamtape.get_download_link,
        videoservers.mp4upload.get_download_link,
        videoservers.vidcdn.get_download_link,
    ]

    # Get the best available download link!
    for get_download_link_func in download_link_functions:
        dl = get_download_link_func(ep)
        if dl:
            return dl

    return None
