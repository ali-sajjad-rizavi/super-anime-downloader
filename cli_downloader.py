import os, glob

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
		#..........
		if os.path.isfile(f'downloaded/{filename}') and not os.path.isfile(f'downloaded/{filename}.aria2'):
			return
		#-------------#if os.name == 'posix': subprocess.call(cmd.split())
		while True:
			try:
				os.system(cmd)
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
			#---
			extension = '.mp4'
			if '.m3u8' in download_link:
				extension = '.m3u8'
			self.__downloadEpisode(filename=episodeDict['episode-title']+extension, download_link=download_link)
		self.__retryFailedDownloads()

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
					os.system(command)
					break
				except KeyboardInterrupt: input('\nDownloader is paused. PRESS [ENTER] TO CONTINUE...')

	def __del__(self):
		if len(glob.glob('downloaded/*.aria2')) != 0:
			return
		os.rename('downloaded', self.anime_dict['anime-title'])
		#---
		if os.path.isfile('failed.txt'):
			os.remove('failed.txt')



###----------------###
#### MAIN ROUTINE #### Example: https://www19.gogoanime.io/category/makura-no-danshi
###----------------###

def main():
    print("\t\t|======================|")
    print("\t\t| CLI ANIME DOWNLOADER |")
    print("\t\t|======================|\n")
    #
    searchInput = input(" - Enter Anime name/URL: ")
    if 'gogoanime' in searchInput:
    	anime_scraper = GogoanimeScraper(searchInput)
    else:
    	print('\n\tResults:\n')
    	anime_search_results = GogoanimeScraper.searchAnime(query=searchInput)
    	[print(f'\t {i+1}) {anime_search_results[i][0]}') for i in range(len(anime_search_results))]
    	selected_index = int(input('\n- Select your option: ')) - 1
    	anime_scraper = GogoanimeScraper(anime_search_results[selected_index][1])
    #
    print("\t -FOUND:", anime_scraper.episode_count, " Episodes in TOTAL!\n")
    #-----
    start_ep = int(input("\t - Start From Episode: "))
    end_ep = int(input("\t - End At Episode: "))
    print('----------------------------------------------------------------------------------')
    print(f'- Scraping episode video links from {start_ep} to {end_ep}, wait for a while...')
    anime_scraper.scrapeEpisodes(start=start_ep, end=end_ep)
    #
    print("\nStarting Download using aria2...\n")
    downloader = Downloader(anime_scraper.dataDict)
    downloader.downloadAnime()
    print("=======================================================")
    print("-------------------- COMPLETED !!! --------------------")
    print("=======================================================")
    #
    print("Done!")

if __name__ == '__main__':
	main()
