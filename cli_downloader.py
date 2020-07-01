import os, subprocess, glob

from gogoanime import AnimeScraper as GogoanimeScraper
import download_link_builder




class Downloader:
	def __init__(self, anime_dictionary):
		if os.path.isfile('failed.txt'):
			os.remove('failed.txt')
		self.anime_dict = anime_dictionary

	def __downloadEpisode(self, filename='episode.mp4', download_link='download-url'):
		print("============================================================================")
		print(" DOWNLOADING EPISODE:", filename)
		print("============================================================================")
		options = f'-x 10 --max-tries=5 --retry-wait=10 --check-certificate=false -d downloaded -o "{filename}"'
		cmd = f'aria2c {download_link} {options}'
		print(cmd)
		input()
		#..........
		if os.path.isfile(f'downloaded/{filename}') and not os.path.isfile(f'downloaded/{episode_filename}.aria2'):
			return
		#-------------
		while True:
			try:
				if os.name == 'posix': subprocess.call(cmd.split())
				if not os.name == 'posix': os.system(cmd)
				break
			except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")
		#-------------
		if os.path.isfile("downloaded/" + filename + ".aria2"):
			open('failed.txt', 'a').write(cmd + '\n')

	def downloadAnime(self):
		for episodeDict in self.anime_dict['scraped-episodes']:
			download_link = download_link_builder.get_available_download_link(episodeDict)
			if download_link == 'unavailable':
				continue
			self.__downloadEpisode(filename=episodeDict['episode-title']+'.mp4', download_link=download_link)
		self.__retryFailedDownloads()
		if len(glob.glob('downloaded/*.aria2')) != 0:
			return
		os.rename('downloaded', self.anime_dict['anime-title'])

	def __retryFailedDownloads(self):
		if not os.path.isfile('failed.txt'):
			return
		print('-------------------------------------')
		print('- Retrying failed downloads')
		print('-------------------------------------')
		commands = open('failed.txt', 'r').read().strip().split('\n')
		for command in commands:
			while True:
				try:
					if os.name == 'posix': subprocess.call(command.split())
					if not os.name == 'posix': os.system(command)
					break
				except KeyboardInterrupt: input('\nDownloader is paused. PRESS [ENTER] TO CONTINUE...')

	def __del__(self):
		if os.path.isfile('failed.txt'):
			os.remove('failed.txt')



###----------------###
#### MAIN ROUTINE ####
###----------------###

def main():
    print("\t\t|======================|")
    print("\t\t| CLI ANIME DOWNLOADER |")
    print("\t\t|======================|\n")
    #
    anime_scraper = GogoanimeScraper(input(" - Enter Anime main-page URL: "))
    print("\t -FOUND:", anime_scraper.episode_count, " Episodes in TOTAL!\n")
    anime_scraper.scrapeEpisodes(int(input("\t - Start From Episode: ")), int(input("\t - End At Episode: ")))
    #
    print("\nStarting Download using aria2...\n")
    downloader = Downloader(anime_scraper.dataDict)
    downloader.downloadAnime()
    print("=======================================================")
    print("-------------------- COMPLETED !!! --------------------")
    print("=======================================================")
    downloader.retryFailedDownloads()
    #
    print("Done!")

if __name__ == '__main__':
	main()
