import os
import subprocess

from anime import Anime
from episode import Episode


class Downloader:
	def __init__(self, anime):
		self.anime = anime

	def __downloadEpisode(self, episode):
		if episode.is_mp4Upload_available() == False:
			print("\n", "::: COULD NOT FIND ::: EPISODE:-", episode.getTitle(), "| Server=MP4-UPLOAD\n")
		else:
			print("============================================================================")
			print(" DOWNLOADING EPISODE:", episode.getTitle().replace(' ', '_'))
			print("============================================================================")
			options = " -x 10 --max-tries=5 --retry-wait=10 --check-certificate=false -d downloaded -o "
			episode_filename = episode.getTitle().replace(' ', '_') + ".mp4"
			cmd = "aria2c " + episode.fetchDownloadLink() + options + episode_filename
			#..........
			#..........
			if os.path.isfile("downloaded/" + episode_filename) and not os.path.isfile("downloaded/" + episode_filename + ".aria2"):
				return
			#-------------
			while True:
				try:
					if os.name == 'posix': subprocess.call(cmd.split())
					if not os.name == 'posix': os.system(cmd)
					break
				except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")
			#-------------
			if os.path.isfile("downloaded/" + episode_filename + ".aria2"):
				self.failed_downloads_file.write(cmd + '\n')

	def downloadAnime(self):
		self.failed_downloads_file = open('failed.txt', 'w', encoding='utf-8')
		for episode in self.anime.getEpisodeList():
			self.__downloadEpisode(episode)
		self.failed_downloads_file.close()
		self.anime.finalizeAnime()

	def retryFailedDownloads(self):
		commands = open('failed.txt', 'r').read().strip().split('\n')
		for command in commands:
			while True:
				try:
					if os.name == 'posix': subprocess.call(command.split())
					if not os.name == 'posix': os.system(command)
					break
				except KeyboardInterrupt: input('\nDownloader is paused. PRESS [ENTER] TO CONTINUE...')



###----------------###
#### MAIN ROUTINE ####
###----------------###

def main():
    print("\t\t|==================|")
    print("\t\t| ANIME DOWNLOADER |")
    print("\t\t|==================|\n")
    #
    theanime = Anime(input(" - Enter Anime main-page URL: "))
    print("\t -FOUND:", theanime.getTotalEpisodeCount(), " Episodes in TOTAL!\n")
    theanime.collectEpisodes(int(input("\t - Start From Episode: ")), int(input("\t - End At Episode: ")))
    print("\nStarting Download using aria2...\n")
    theanime.displayEpisodes()
    #
    downloader = Downloader(theanime)
    downloader.downloadAnime()
    print("=======================================================")
    print("-------------------- COMPLETED !!! --------------------")
    print("=======================================================")
    downloader.retryFailedDownloads()
    #
    print("Done!")

if __name__ == '__main__':
	main()