import requests as REQ
from bs4 import BeautifulSoup as BS
import re as REGEX
import os as OS
import subprocess as SP

completion_flag = False

#-------------------------------------------

class FailedContainer:
    failedCommandsList = []
    def addFailedCommand(cmd):
        FailedContainer.failedCommandsList.append(cmd)
    def retryFailedDownloads():
        if len(FailedContainer.failedCommandsList) == 0:
            return
        print("\n\n\n There were", len(FailedContainer.failedCommandsList), "failed downloads which can be resumed...")
        print(" If they fail again, there might be a server issue with these links.")
        while True:
            choice = input(" Do you want to retry downloading these Episodes? (Y/N): ")
            if choice == 'y' or choice == 'Y':
                break
            if choice == 'n' or choice == 'N':
                return
        i = 1
        for cmd in FailedContainer.failedCommandsList:
            print("\n===========[ Retrying download #", i, "]\n")
            OS.system(cmd)
            i += 1

#-------------------------------------------
class Anime:
    def __init__(self, url):
        print("Initializing...")
        animeSoup = BS(REQ.get(url).text, 'html.parser')
        animeID = animeSoup.find(id="movie_id")['value']
        animeAlias = animeSoup.find(id="alias_anime")['value']
        animeLastEp = animeSoup.find(id="episode_page").find_all('a')[-1]['ep_end']
        #----private data members------
        self.__title = animeSoup.title.text.replace("at Gogoanime", '').strip()
        self.__mainpageURL = url
        self.__ajaxURL = "https://ajax.gogocdn.net/ajax/load-list-episode?ep_start=0&ep_end=" + animeLastEp + "&id=" + animeID + "&default_ep=0&alias=" + animeAlias
        self.__ajaxSoup = BS(REQ.get(self.__ajaxURL).text, 'html.parser')
        self.__eptotal = len(self.__ajaxSoup.find_all('a'))
        #------------------------------

    def getTitle(self):
        return self.__title
    def getURL(self):
        return self.__mainpageURL
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

    def downloadEpisodes(self):
        for episode in reversed(self.__episodeList):
            episode.download()
    def displayEpisodes(self):
        for ep in reversed(self.__episodeList):
            print(ep.getTitle())
    def displayDownloadLinks(self):
        for epis in reversed(self.__episodeList):
            epis.get_Mp4UploadDownloadLink()
    def finalizeAnime(self):
        for epis in self.__episodeList:
            isEpisFile = OS.path.isfile(OS.path.join("downloaded", epis.getTitle().replace(' ', '_') + ".mp4"))
            isAriaFile = OS.path.isfile(OS.path.join("downloaded", epis.getTitle().replace(' ', '_') + ".mp4.aria2"))
            if not isEpisFile or isAriaFile: return
        OS.rename("downloaded", self.__title)

    def playEpisodesOnline(self):
        pass
#-------------------------------------------
class Episode:
    def __init__(self, title, url):
        self.__title = title
        self.__url = url
        mp4ElementList = BS(REQ.get(url).text, 'html.parser').find_all('li', {'class':'mp4'})
        if len(mp4ElementList) is 0:
            self.__mp4uploadEmbed = "not_found"
        else:
            self.__mp4uploadEmbed = mp4ElementList[0].find('a')['data-video']

    def get_Mp4UploadDownloadLink(self):
        scripts = BS(REQ.get(self.__mp4uploadEmbed).text, 'html.parser').find_all('script', type="text/javascript")
        evalText = [script.text for script in scripts if "navigator" in script.text][0]
        #evalText = scripts[len(scripts)-1].text
        evalItems = evalText.split('|')
        del evalItems[:evalItems.index('navigator')+1]
        videoID = [a for a in evalItems if len(a)>30][0]
        #
        evalItems = evalText.split('|')
        w3strPossiblesList = [s for s in evalItems if REGEX.match('s\d+$', s) or REGEX.match('www\d+$', s)]
        print("\n", w3strPossiblesList, "\n")
        w3str = "www"
        if len(w3strPossiblesList) is not 0:
            w3str = max(w3strPossiblesList, key=len)
        #
        retstr = "https://" + w3str + ".mp4upload.com:" + evalItems[evalItems.index(videoID)+1] + "/d/" + videoID + "/video.mp4"
        print("Got:-", retstr)
        return retstr

    def getTitle(self):
        return self.__title
    def download(self):
        if self.__mp4uploadEmbed is "not_found":
            print("\n", "::: COULD NOT FIND ::: EPISODE:-", self.__title, "| Server=MP4-UPLOAD\n")
        else:
            print("============================================================================")
            print(" DOWNLOADING EPISODE:", self.__title.replace(' ', '_'))
            print("============================================================================")
            options = " -x 10 --max-tries=5 --retry-wait=10 --check-certificate=false -d downloaded -o "
            episode_filename = self.__title.replace(' ', '_') + ".mp4"
            cmd = "aria2c " + self.get_Mp4UploadDownloadLink() + options + episode_filename
            if OS.path.isfile(OS.path.join("downloaded", episode_filename)) and not OS.path.isfile(OS.path.join("downloaded", episode_filename + ".aria2")):
                return
            if OS.name == 'posix':
                while True:
                    try:
                        SP.call(cmd.split())
                        break
                    except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")
            else:
                while True:
                    try:
                        OS.system(cmd)
                        break
                    except KeyboardInterrupt: input("\nDownloader is paused. PRESS [ENTER] TO CONTINUE...")
            if OS.path.isfile(OS.path.join("downloaded", self.__title.replace(' ', '_') + ".mp4.aria2")):
                FailedContainer.addFailedCommand(cmd)
#--------------------------------------------------------------------

###----------------###
#### MAIN ROUTINE ####
###----------------###

def main():
    print("\t\t|==================|")
    print("\t\t| ANIME DOWNLOADER |")
    print("\t\t|==================|\n")
    theanime = Anime(input(" - Enter Anime main-page URL: "))
    print("\t -FOUND:", theanime.getTotalEpisodeCount(), " Episodes in TOTAL!\n")
    theanime.collectEpisodes(int(input("\t - Start From Episode: ")), int(input("\t - End At Episode: ")))
    print("\nStarting Download using aria2...\n")
    theanime.displayEpisodes()
    #theanime.displayDownloadLinks()
    theanime.downloadEpisodes()
    print("=======================================================")
    print("-------------------- COMPLETED !!! --------------------")
    print("=======================================================")
    FailedContainer.retryFailedDownloads()
    print("Checking downloads...")
    theanime.finalizeAnime()
    print("Done!")

main()
