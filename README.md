# youtube-coub-dl-mac
Simple program with GUI for downloading videos and audio from coub.com and youtube.com for mac.

![EasyDownloader Screenshot1](https://github.com/steam3d/youtube-coub-dl-mac/blob/master/ReadmeMedia/1.jpg)
![EasyDownloader Screenshot2](https://github.com/steam3d/youtube-coub-dl-mac/blob/master/ReadmeMedia/2.jpg)

## How it works

1. Copy youtube or coub link
2. Choose one of the items
 	* Audio - Downloading best quality audio and convert to mp3
	* Video - Downloading best quality video and convert to mp4
	* Au+vi - Downloading 720p video with audio (does not support coub.com links)
3. Check `~/Downloads` folder or click on the notification

> This software uses libraries from the FFmpeg project under the LGPLv2.1

## [Download Easy Downloader](https://github.com/steam3d/youtube-coub-dl-mac/releases)

## How to create a program from source files
To install it use a py2app package

	pip3 install py2app

Download [ffmpeg](https://www.ffmpeg.org/) and put it to folder with source

From folder with source code run a command

	python3 setup.py py2app

## What packages were used

* [pyperclip](https://github.com/asweigart/pyperclip)
* [rumps](https://github.com/jaredks/rumps)
* [pync](https://github.com/SeTeM/pync)
* [youtube-dl](https://github.com/rg3/youtube-dl)
* [ffmpeg](https://www.ffmpeg.org/)





