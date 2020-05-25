from bs4 import BeautifulSoup
import requests


class Mp4UploadGenerator:
	def __init__(self, embed_url):
		self.embed_url = embed_url

	def fetchDownloadLink(self):
		scripts = BeautifulSoup(requests.get(self.embed_url).text, 'html.parser').find_all('script', type="text/javascript")
		evalText = [script.text for script in scripts if "navigator" in script.text][0]
		#evalText = scripts[len(scripts)-1].text
		evalItems = evalText.split('|')
		del evalItems[:evalItems.index('navigator')+1]
		videoID = [a for a in evalItems if len(a)>30][0]
		#
		evalItems = evalText.split('|')
		w3strPossiblesList = [s for s in evalItems if REGEX.match('s\d+$', s) or REGEX.match('www\d+$', s)]
		w3str = "www"
		if len(w3strPossiblesList) is not 0:
			w3str = max(w3strPossiblesList, key=len)
		#
		retstr = "https://" + w3str + ".mp4upload.com:" + evalItems[evalItems.index(videoID)+1] + "/d/" + videoID + "/video.mp4"
		return retstr