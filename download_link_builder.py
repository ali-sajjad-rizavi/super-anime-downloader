from videoservers import mp4upload
from videoservers import vidcdn
from videoservers import mixdrop


def get_available_download_link(episode_dict):
	''' Mp4Upload '''
	if 'mp4' in episode_dict['embed-servers'].keys():
		download_link = mp4upload.get_download_link(episode_dict['embed-servers']['mp4'])
		if download_link is not None:
			return download_link

	''' VidCDN '''
	if 'vidcdn' in episode_dict['embed-servers'].keys():
		download_link = vidcdn.get_download_link(episode_dict['embed-servers']['vidcdn'])
		if download_link is not None:
			return download_link

	''' Mixdrop '''
	if 'mixdrop' in episode_dict['embed-servers'].keys():
		download_link = mixdrop.get_download_link(episode_dict['embed-servers']['mixdrop'])
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