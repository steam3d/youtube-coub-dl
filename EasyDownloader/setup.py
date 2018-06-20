from setuptools import setup

APP = ['menu_bar.py']
APP_NAME = "Easy Downloader"
DATA_FILES = ["ffmpeg", "ffprobe",'tray.png','traydl.png','app.icns']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Download from Youtube",
        'CFBundleIdentifier': "com.steam3d.osx.ed",
        'CFBundleVersion': "0.0.1",
        'CFBundleShortVersionString': "0.0.3",
        'NSHumanReadableCopyright': u"The program is written by Alexander Maslov"        
    },
    'packages': ['rumps','pync'],
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
