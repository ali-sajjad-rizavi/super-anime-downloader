import os, glob

from gogoanime import AnimeScraper as GogoanimeScraper
import download_link_builder


class Downloader:
    def __init__(self, anime_dict: dict):
        """Constructor of Downloader class"""
        if os.path.isfile("failed.txt"):
            os.remove("failed.txt")
        self.anime_dict = anime_dict

    def download_anime(self):
        """
        Downloads all episodes which were scraped
        """
        for episodeDict in self.anime_dict["scraped-episodes"]:
            download_link = download_link_builder.get_available_download_link(episodeDict)

            # Skip if episode download URL is not available
            if not download_link:
                continue

            # TODO: Implement a technique to download .m3u8 files.
            file_extension = "m3u8" if "m3u8" in download_link else "mp4"

            ep_title = episodeDict["episode-title"]
            Downloader.download_episode(
                filename=f"{ep_title}.{file_extension}",
                download_link=download_link,
            )

        self.retry_failed_download_commands()

    @staticmethod
    def download_episode(filename: str, download_link: str):
        """
        Downloads a single episode using aria2 downloader

        :param filename: Name of video file to be downloaded
        :param download_link: Download URL of video
        """
        print("============================================================================")
        print(f" DOWNLOADING EPISODE: {filename}")
        print("============================================================================")

        # Command to use on terminal/cmd for downloading the video using aria2
        options = f'-x 10 --max-tries=5 --retry-wait=10 --check-certificate=false -d downloaded -o "{filename}"'
        cmd = f'aria2c "{download_link}" {options}'

        # Skip this episode download if the download is already completed
        if os.path.isfile(f"downloaded/{filename}") and not os.path.isfile(
            f"downloaded/{filename}.aria2"
        ):
            return

        # Catch Ctrl+C to pause the download, then resume download on pressing ENTER
        while True:
            try:
                os.system(cmd)
                break
            except KeyboardInterrupt:
                input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")

        # If at the end, the .aria2 file for this episode still exists, it means download
        # was failed at some point. So add the command to "failed.txt" file.
        if os.path.isfile(f"downloaded/{filename}.aria2"):
            open("failed.txt", "a").write(cmd + "\n")

    @staticmethod
    def retry_failed_download_commands():
        """
        Retries all failed downloads by running the failed commands in "failed.txt" file.
        """
        if not os.path.isfile("failed.txt"):
            return

        print("-------------------------------------")
        print("- Retrying failed downloads")
        print("-------------------------------------")

        failed_commands = open("failed.txt", "r").read().strip().split("\n")

        for cmd in failed_commands:
            # Catch Ctrl+C to pause the download, then resume download on pressing ENTER
            while True:
                try:
                    os.system(cmd)
                    break
                except KeyboardInterrupt:
                    input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")

    def __del__(self):
        if len(glob.glob("downloaded/*.aria2")) != 0:
            return
        os.rename("downloaded", self.anime_dict["anime-title"])
        # ---
        if os.path.isfile("failed.txt"):
            os.remove("failed.txt")


# Example: https://www19.gogoanime.io/category/makura-no-danshi
def main():
    print("\t\t|======================|")
    print("\t\t| CLI ANIME DOWNLOADER |")
    print("\t\t|======================|\n")

    search_input = input(" - Enter Anime name/URL: ")

    # Create anime scraper object using search by name, or the anime URL
    if "gogoanime" in search_input:
        anime_scraper = GogoanimeScraper(search_input)
    else:
        anime_search_results = GogoanimeScraper.search_anime(search_input)

        # Display search results
        print("\n\tResults:\n")
        for i in range(len(anime_search_results)):
            print(f"\t {i + 1}) {anime_search_results[i][0]}")

        selected_index = int(input("\n- Select your option: ")) - 1

        # Create anime scraper object based on the selected choice
        anime_scraper = GogoanimeScraper(anime_search_results[selected_index][1])

    print("\t -FOUND:", anime_scraper.episode_count, " Episodes in TOTAL!\n")

    start_ep = int(input("\t - Start From Episode: "))
    end_ep = int(input("\t - End At Episode: "))

    print("----------------------------------------------------------------------------------")
    print(f"- Scraping episode video links from {start_ep} to {end_ep}, wait for a while...")

    anime_scraper.scrape_episodes(start=start_ep, end=end_ep)

    print("\nStarting Download using aria2...\n")

    downloader = Downloader(anime_scraper.dataDict)
    downloader.download_anime()

    print("=======================================================")
    print("-------------------- COMPLETED !!! --------------------")
    print("=======================================================")

    print("Done!")
    input("- Press [ENTER] to quit...")


if __name__ == "__main__":
    main()
