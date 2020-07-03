# super-anime-downloader
This repository consists of a python console application (GUI will be added soon) which takes a Anime URL as input and downloads the range of episodes you specify.

# Supported Operating Systems:
- Windows XP/7/8/8.1/10
- Linux (Debian, Fedora, Arch etc.)
- MacOS
- Android (Using Termux: https://play.google.com/store/apps/details?id=com.termux )

# Dependencies
- Python: Download and install python3 ( https://www.python.org/downloads/ ).
- Aria2C: This program uses aria2 command-line (CLI) downloader ( https://aria2.github.io/ ).
You can put the aria2c executable ('aria2.exe' or 'aria2c') inside  the current directory, or add it in PATH environment variable.
Linux users can install using this command:
```
sudo apt-get install aria2
```

# Packages needed
After installing python, you need these packages:
- requests
- bs4 (BeautifulSoup)
You can insatll them using pip.
```
pip install requests
pip install bs4
```

# HOW TO USE?

Download the repository .zip file, extract it, then open "cli_downloader.py" (open with Python) present inside the repository folder.
OR
Just clone it and run the code after moving inside the repository using:
```
git clone https://github.com/ali-sajjad-rizavi/super-anime-downloader.git
cd super-anime-downloader
python cli_downloader.py
```

Just copy the link of the Anime you want to download. For now, this script only supports
the Anime links from GoGoAnime (See: https://www.gogoanime.io) but more websites support
will be added later.

After copying URL:
- Paste the Anime URL in the terminal/command-prompt and press ENTER.
- Provide the range of episodes you want to download.

***PAUSE AN ONGOING DOWNLOAD:***
Press [Ctrl+C] to pause download. To exit, press [Ctrl+C] again.

***RESUME DOWNLOADS:***
Run program again, already downloaded episodes will not be downloaded again.
The episodes which are partially downloaded, will automatically resume from where they stopped.

***Note:-*** The anime will be downloaded in the current working directory (current folder).

# Important note!

I am not responsible for the content you download using this script.
The downloaded videos will by present in "CurrentWorkingDirectory/downloaded" folder.

Please report if there are any issues so that this tool can be further improved!
