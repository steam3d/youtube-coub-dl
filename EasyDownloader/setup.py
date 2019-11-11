from setuptools import setup

APP = ['easydownloader.py']
APP_NAME = "Easy Downloader"
DATA_FILES = ['data','dl.py','dlffmpeg.py','mac_notification.py','exceptions.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'data/app.icns',
    'plist': {
        'LSUIElement': True,
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Download from Youtube and Coub",
        'CFBundleIdentifier': "com.steam3d.osx.ed",
        'CFBundleVersion': "0.2.2",
        'CFBundleShortVersionString': "0.2.2",
        'NSHumanReadableCopyright': u"The program is written by Alexander Maslov"        
    },
    'packages': ['pyperclip','PIL','pync'],
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
