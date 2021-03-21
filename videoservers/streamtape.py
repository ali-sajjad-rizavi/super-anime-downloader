from bs4 import BeautifulSoup
import requests


my_headers = {}
my_headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'



def get_download_link(embed_url):
	try:
		response = requests.get(embed_url, headers=my_headers)
		soup = BeautifulSoup(response.text, 'html.parser')
		text = [str(script) for script in soup.find_all('script') if ').innerHTML' in str(script)][0]
		text = ''.join(text.rstrip('</script>').lstrip('<script>').split())
		text = text.split('innerHTML=')[1].rstrip(';')
		text = ''.join([ substr.strip('"').strip("'") for substr in text.split('+') ])
		download_link = f'https:{text}'
		return download_link
	except Exception as e:
		print(e)
		return None



######
######
######

if __name__ == '__main__':
	print(get_download_link('https://streamtape.com/e/YqKyKxg23jivJDB/world-trigger-2nd-season-episode-10.mp4'))