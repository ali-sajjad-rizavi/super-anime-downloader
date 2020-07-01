from bs4 import BeautifulSoup
import requests
import re as RegExp


def get_mp4upload_download_link(embed_url):
	scripts = BeautifulSoup(requests.get(embed_url).text, 'html.parser').find_all('script', type="text/javascript")
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
	return 'https://{}.mp4upload.com:{}/d/{}/video.mp4'.format(w3str, evalItems[evalItems.index(videoID)+1], videoID)

######
######
######

# A sample Mp4Upload embedded URL: https://www.mp4upload.com/embed-99r0hr81zk9k.html

def main():
	print('\t\t=====================')
	print('\t\t Mp4Upload Generator')
	print('\t\t=====================')
	try:
		download_link = get_mp4upload_download_link(input('\t- Enter Mp4Upload Embed URL: '))
		print('- The generated download link: ', download_link)
	except Exception as e:
		print('\tSomething went wrong while generating the Download link!')
		print('Error message: ', e)

if __name__ == '__main__':
	main()
