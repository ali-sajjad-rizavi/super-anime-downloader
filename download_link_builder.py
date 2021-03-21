from videoservers import mp4upload
from videoservers import vidcdn
from videoservers import mixdrop


def get_available_download_link(episode_dict):
	if 'mp4' in episode_dict['embed-servers'].keys():
		download_link = mp4upload.get_mp4upload_download_link(episode_dict['embed-servers']['mp4'])
		if download_link is not None:
			return download_link
	if 'vidcdn' in episode_dict['embed-servers'].keys():
		download_link = vidcdn.get_vidcdn_download_link(episode_dict['embed-servers']['vidcdn'])
		if download_link is not None:
			return download_link
	if 'mixdrop' in episode_dict['embed-servers'].keys():
		download_link = mixdrop.get_download_link(episode_dict['embed-servers']['mixdrop'])
		if download_link is not None:
			return mixdrop.get_download_link(episode_dict['embed-servers']['mixdrop'])
	return 'unavailable'


######
######
######

def main():
	print('This is an import script')

if __name__ == '__main__':
	main()