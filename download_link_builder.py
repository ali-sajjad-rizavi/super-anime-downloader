from videoservers import mp4upload
from videoservers import vidcdn
from videoservers import mixdrop
from videoservers import streamtape


def get_available_download_link(episode_dict):
	''' Mixdrop '''
	if 'mixdrop' in episode_dict['embed-servers'].keys():
		download_link = mixdrop.get_download_link(episode_dict['embed-servers']['mixdrop'])
		if download_link is not None:
			return download_link

	''' Streamtape '''
	if 'streamtape' in episode_dict['embed-servers'].keys():
		download_link = streamtape.get_download_link()
		if download_link is not None:
			return download_link

	''' Mp4Upload '''
	if 'mp4upload' in episode_dict['embed-servers'].keys():
		download_link = mp4upload.get_download_link(episode_dict['embed-servers']['mp4'])
		if download_link is not None:
			return download_link

	''' VidCDN '''
	if 'vidcdn' in episode_dict['embed-servers'].keys():
		download_link = vidcdn.get_download_link(episode_dict['embed-servers']['vidcdn'])
		if download_link is not None:
			return download_link
	
	return 'unavailable'


######
######
######

def main():
	print('This is an import script')

if __name__ == '__main__':
	main()