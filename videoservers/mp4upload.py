from bs4 import BeautifulSoup
import requests
import re as RegExp


class Mp4UploadGenerator:
	def __init__(self, embed_url):
		self.embed_url = embed_url

	def fetchDownloadLink(self):
		scripts = BeautifulSoup(requests.get(self.embed_url).text, 'html.parser').find_all('script', type="text/javascript")
		evalText = [script.text for script in scripts if "|embed|" in script.text][0]
		#evalText = scripts[len(scripts)-1].text
		evalItems = evalText.split('|')
		del evalItems[:evalItems.index('mp4upload')+1]
		videoID = [a for a in evalItems if len(a)>30][0]
		#
		evalItems = evalText.split('|')
		w3strPossiblesList = [s for s in evalItems if RegExp.match('s\d+$', s) or RegExp.match('www\d+$', s)]
		w3str = "www"
		if len(w3strPossiblesList) is not 0:
			w3str = max(w3strPossiblesList, key=len)
		#
		retstr = "https://" + w3str + ".mp4upload.com:" + evalItems[evalItems.index(videoID)+1] + "/d/" + videoID + "/video.mp4"
		return retstr

######
######
######

# A sample Mp4Upload embedded URL: https://www.mp4upload.com/embed-99r0hr81zk9k.html

def main():
	print('\t\t=====================')
	print('\t\t Mp4Upload Generator')
	print('\t\t=====================')
	mp4upload_generator = Mp4UploadGenerator(input('\t- Enter Mp4Upload Embed URL: '))
	download_link = mp4upload_generator.fetchDownloadLink()
	try:
		download_link = mp4upload_generator.fetchDownloadLink()
		print('- The generated download link: ', download_link)
	except Exception as e:
		print('\tSomething went wrong while generating the Download link!')
		print('Error says: ', e)

if __name__ == '__main__':
	main()
