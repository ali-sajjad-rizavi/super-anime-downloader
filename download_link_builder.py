from videoservers import mp4upload


def get_available_download_link(episode_dict):
	if 'mp4' in episode_dict['embed-servers'].keys():
		return mp4upload.get_mp4upload_download_link(episode_dict['embed-servers']['mp4'])
	return 'unavailable'


######
######
######

def main():
	print('This is an import script')

if __name__ == '__main__':
	main()