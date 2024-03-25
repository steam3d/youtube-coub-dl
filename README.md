# youtube-coub-dl
Simple script with GUI for downloading videos and audio from coub.com and youtube.com for mac, windows and linux.
Easy downloader has standalone app for mac. For windows and linux there is only a python script.

![EasyDownloader Screenshot1](https://github.com/steam3d/youtube-coub-dl-mac/blob/master/ReadmeMedia/1.jpg)
![EasyDownloader Screenshot2](https://github.com/steam3d/youtube-coub-dl-mac/blob/master/ReadmeMedia/2.jpg)

## How it works

1. Copy youtube or coub link
2. Choose one of the items
 	* Audio - Downloading best quality audio and convert to mp3
	* Video - Downloading best quality video and convert to mp4
	* Au+vi - Downloading 720p video with audio (does not support coub.com links)
3. Check `~/Downloads` folder or click on the notification (Linux option does not have a notification).

> This software uses libraries from the [FFmpeg](https://www.ffmpeg.org/) project under the LGPLv2.1

## [Download Easy Downloader for MAC](https://github.com/steam3d/youtube-coub-dl-mac/releases)

## How to create a program from source files for MAC and WINDOWS
To install it use a py2app package

	pip3 install py2app


From folder with source code run a command

	python3 setup.py py2app

## Hot to run script from python

Base GUI	
	
	pip install pystray

Youtube-dl

	pip install youtube-dl	


Clipboard for mac and windows

	pip install pyperclip 
	
Clipboard for linux

	sudo apt-get insall xclip

Notification for mac

	pip install pync
	
Notification for windows

	pip install win10toast

Download ffmpeg and put it to folder with script

## Build

Using PyInstaller Windows

	pyinstaller easydownloader.spec --onefile

Using p2app Mac

	Not written yet 
 
### p2app issue: Header Mach-O too large

Remove files from this folder which cause the error

	/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/PIL/.dylibs/

## What packages were used

* [pyperclip](https://github.com/asweigart/pyperclip)
* [pync](https://github.com/SeTeM/pync)
* [pystray](https://github.com/moses-palmer/pystray)
* [youtube-dl](https://github.com/rg3/youtube-dl)
* [ffmpeg](https://www.ffmpeg.org/)





