import requests
from bs4 import BeautifulSoup
from videoservers.mp4upload import Mp4UploadGenerator


class Episode:
    def __init__(self, title, url):
        self.__title = title
        self.__url = url
        mp4ElementList = BeautifulSoup(requests.get(url).text, 'html.parser').find_all('li', {'class':'mp4'})
        if len(mp4ElementList) is 0:
            self.__mp4uploadEmbed = "not_found"
            self.__mp4upload_generator = None
        else:
            self.__mp4uploadEmbed = mp4ElementList[0].find('a')['data-video']
            self.__mp4upload_generator = Mp4UploadGenerator(self.__mp4uploadEmbed)

    def fetchDownloadLink(self):
        return self.__mp4upload_generator.fetchDownloadLink()

    def getTitle(self):
        return self.__title

######
######
######

# A sample episode URL: https://www19.gogoanime.io/sin-nanatsu-no-taizai-dub-episode-1

def main():
    print('\t\t===================')
    print('\t\t GoGoAnime Episode')
    print('\t\t===================')
    episode = None
    try:
        episode = Episode('Sample episode', input('\t- Enter episode URL: '))
        print(' Download Link:', episode.fetchDownloadLink())
    except Exception as e:
        print('\t- Something went wrong while parsing episode URL!')
        print(' Error says:', e)

if __name__ == '__main__':
    main()