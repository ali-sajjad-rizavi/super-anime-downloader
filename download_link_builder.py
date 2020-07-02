from videoservers import mp4upload
from videoservers import vidcdn


def get_available_download_link(episode_dict):
	if 'mp4' in episode_dict['embed-servers'].keys():
		return mp4upload.get_mp4upload_download_link(episode_dict['embed-servers']['mp4'])
	if 'vidcdn' in episode_dict['embed-servers'].keys():
		return vidcdn.get_vidcdn_download_link(episode_dict['embed-servers']['vidcdn'])
	return 'unavailable'


######
######
######

def main():
	print('This is an import script')

if __name__ == '__main__':
	main()