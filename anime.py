import requests
from bs4 import BeautifulSoup
import os
from episode import Episode


class Anime:
    def __init__(self, url):
        print("Initializing...")
        animeSoup = BeautifulSoup(requests.get(url).text, 'html.parser')
        animeID = animeSoup.find(id="movie_id")['value']
        animeAlias = animeSoup.find(id="alias_anime")['value']
        animeLastEp = animeSoup.find(id="episode_page").find_all('a')[-1]['ep_end']
        #----private data members------
        self.__title = animeSoup.title.text.replace("at Gogoanime", '').strip()
        self.__mainpageURL = url
        self.__ajaxURL = "https://ajax.gogocdn.net/ajax/load-list-episode?ep_start=0&ep_end=" + animeLastEp + "&id=" + animeID + "&default_ep=0&alias=" + animeAlias
        self.__ajaxSoup = BeautifulSoup(requests.get(self.__ajaxURL).text, 'html.parser')
        self.__eptotal = len(self.__ajaxSoup.find_all('a'))
        #------------------------------

    def getTitle(self):
        return self.__title

    def getTotalEpisodeCount(self):
        return self.__eptotal

    def collectAllEpisodes(self):
        self.__episodeList = []
        for li in self.__ajaxSoup.find_all('li'):
            self.__episodeList.insert(0, Episode(self.__title + " - " + " ".join(li.text.split()), "https://www.gogoanime.io" + li.find('a')['href'].strip()))

    def collectEpisodes(self, start, end):
        self.__episodeList = []
        for li in self.__ajaxSoup.find_all('li')[-start:-(end+1):-1]:
            self.__episodeList.insert(0, Episode(self.__title + " - " + " ".join(li.text.split()), "https://www.gogoanime.io" + li.find('a')['href'].strip()))

    def displayEpisodes(self):
        for ep in reversed(self.__episodeList):
            print(ep.getTitle())

    def displayDownloadLinks(self):
        for epis in reversed(self.__episodeList):
            print(epis.fetchDownloadLink())

    def finalizeAnime(self):
        for epis in self.__episodeList:
            isEpisFile = OS.path.isfile(OS.path.join("downloaded", epis.getTitle().replace(' ', '_') + ".mp4"))
            isAriaFile = OS.path.isfile(OS.path.join("downloaded", epis.getTitle().replace(' ', '_') + ".mp4.aria2"))
            if not isEpisFile or isAriaFile: return
        OS.rename("downloaded", self.__title)


######
######
######

# A sample anime URL: https://www19.gogoanime.io/category/sin-nanatsu-no-taizai-dub

def main():
    print('\t\t=======')
    print('\t\t Anime')
    print('\t\t=======')
    try:
        anime = Anime(input('\t- Enter Anime URL: '))
        anime.collectAllEpisodes()
        anime.displayDownloadLinks()
    except Exception as e:
        print('\t- Something went wrong!')
        print(' Error says:', e)

if __name__ == '__main__':
    main()