import requests
from bs4 import BeautifulSoup
import re as RegExp

my_headers = {}
my_headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'




def get_vidcdn_download_link(embed_url):
	soup = BeautifulSoup(requests.get(embed_url, headers=my_headers).text, 'html.parser')
	js_text = str(soup.find('div', class_='videocontent'))
	download_link = RegExp.findall('file: \'(.+?)\'', js_text)[0]
	return download_link



######
###### Example: https://vidstreaming.io/load.php?id=OTc2MzI=&title=Boruto%3A+Naruto+Next+Generations+Episode+1
######

def main():
	print('Download link:', input('Enter Vidcdn embed URL: '))

if __name__ == '__main__':
	main()
