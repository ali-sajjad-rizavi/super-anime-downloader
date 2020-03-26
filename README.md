# super-anime-downloader
This repository consists of a python console application (GUI will be added soon) which takes a Anime URL as input and downloads the range of episodes you specify.

# Packages needed
requests, bs4 (BeautifulSoup), subprocess, re
Some of them are available by default, especially if you have anaconda installed.
You can insatll them using pip.

# Dependencies
This program uses aria2 cli downloader.
https://aria2.github.io/

# For Linux users
- Use pip to install needed packages if they aren't installed already.
- Install aria2 using 'sudo apt-get install aria2'
- Run downloader.py and enjoy!!!

# For windows users
- Install anaconda.
- Open anaconda prompt
- Run the pip commands given above
- Download aria2 from official site: https://aria2.github.io/
- In C: drive, make a folder named 'aria2' and paste the contents of downloaded aria2 zip.
- Add the path to aria2c.exe in system environment variable PATH. (e.g. 'C:\aria2\')
- Run downloader.py and enjoy!!!

# Important note!
I am not responsible for the content you download using this script.
The downloaded videos will by present in "CurrentWorkingDirectory/downloaded" folder.

Please report if there are any issues so that this tool can be further improved!
