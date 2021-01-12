import requests, json, os
from bs4 import BeautifulSoup
import re as RegExp


my_headers = {}
my_headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'



class AnimeScraper:
    def __init__(self, url):
        animeSoup = BeautifulSoup(requests.get(url, headers=my_headers).text, 'html.parser')
        animeID = animeSoup.find(id='movie_id')['value']
        animeAlias = animeSoup.find(id='alias_anime')['value']
        animeLastEp = animeSoup.find(id='episode_page').find_all('a')[-1]['ep_end']
        #------------------------------
        ajax_url = f'https://ajax.gogocdn.net/ajax/load-list-episode?ep_start=0&ep_end={animeLastEp}&id={animeID}&default_ep=0&alias={animeAlias}'
        self.dataDict = {}
        #re.sub('[<>?":/|]', '', x)
        self.dataDict['anime-title'] = RegExp.sub('[<>?":/|]', '', animeSoup.title.text.replace('at Gogoanime', '').replace('Watch ', '').strip())
        self.dataDict['anime-url'] = url
        ajaxSoup = BeautifulSoup(requests.get(ajax_url, headers=my_headers).text, 'html.parser')
        self.episode_count = len(ajaxSoup.find_all('a'))
        #------------------------------
        self.dataDict['episodes'] = []
        for li in reversed(ajaxSoup.find_all('li')):
        	episodeDict = {}
        	#re.sub('[<>?":/|]', '', x)
        	#episodeDict['episode-title'] = self.dataDict['anime-title'] + ' - ' + ' '.join(li.text.split())
        	episodeDict['episode-title'] = RegExp.sub('[<>?":/|]', '', '{} - {}'.format(self.dataDict['anime-title'], ' '.join(li.text.split())))
        	episodeDict['episode-url'] = 'https://www.gogoanime.so{}'.format(li.find('a')['href'].strip())
        	self.dataDict['episodes'].append(episodeDict)

    def scrapeEpisodes(self, start=1, end=1):
    	self.dataDict['scraped-episodes'] = []
    	for episodeDict in self.dataDict['episodes'][start-1:end]:
    		scraped_episodeDict = episodeDict
    		soup = BeautifulSoup(requests.get(episodeDict['episode-url'], headers=my_headers).text, 'html.parser')
    		serversList = soup.find('div', {'class':'anime_muti_link'}).find_all('li')[1:]
    		scraped_episodeDict['embed-servers'] = {}
    		for li in serversList:
    			embedUrl = li.find('a')['data-video']
    			if not 'https:' in embedUrl:
    				embedUrl = f'https:{embedUrl}'
    			scraped_episodeDict['embed-servers'][li['class'][0]] = embedUrl
    		#------
    		self.dataDict['scraped-episodes'].append(scraped_episodeDict)
    		print('- Collected:', scraped_episodeDict['episode-title'])

    def saveJSON(self, filename='anime.json'):
    	open(filename, 'w', encoding='utf-8').write(json.dumps(self.dataDict, indent=4, sort_keys=True, ensure_ascii=False))

    # STATIC METHOD
    def searchAnime(query='anime name'):
        response_text = requests.get('https://www.gogoanime.so/search.html?keyword={}'.format(query.replace(' ', '%20'))).text
        p_results = BeautifulSoup(response_text, 'html.parser').find('ul', class_='items').find_all('p', class_='name')[:4]
        paired_results = [(p.find('a')['title'], 'https://www.gogoanime.so{}'.format(p.find('a')['href'])) for p in p_results]
        return paired_results # (title, url) pair list is returned


######
######
######

def main():
	anime_scraper = AnimeScraper(input('Enter Anime URL: '))
	anime_scraper.scrapeEpisodes(start=1, end=1)
	anime_scraper.saveJSON()
	print('- Saved JSON file!')

if __name__ == '__main__':
    main()
