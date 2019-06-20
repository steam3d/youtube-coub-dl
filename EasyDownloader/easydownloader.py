import os, pyperclip, dl, sys, logging
import dlffmpeg
from PIL import Image
from pystray import Icon, Menu as menu, MenuItem as item
from threading import Thread

# sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'FilesDate'))

dlpath = ffmpegpath = iconPath = os.path.join(os.getcwd(), 'data')
fnMask = '/%(title)s-%(id)s.%(ext)s'
fprog = ''  # fix later

menuItems = ['Quit', 'Cancel', ['Only Audio', 'mp3', 0, 'Only Audio'], ['Only Video', 'mp4', 0, 'Only Video'],
             ['Audio+Video', 'mp4+mp3', 0, 'Audio+Video'], 'Download folder']
# for languages
msg = [['Download error', 'The clipboard does not have an youtube or coub link'],
       ['Error', "Can't get file name. Check Donwloads folder"],
       ['Download complete', ''],
       ['Download error', 'The clipboard has a broken link'],
       ['Download folder', ''],
       ['Downloading ffmpeg', 'Please wait until the download is complete'],
       ['Downloading error', 'Something went wrong'],
       ['Download complete', 'Running the app']]

def setlanguage(p):
    global menuItems, msg
    with open(p, 'r',  encoding="utf-8") as f:
        data = f.readlines()
        data = [line.rstrip() for line in data]
        data = [line.split(';') for line in data]
    for i in range(len(menuItems)):
        if type(menuItems[i]) is list:
            menuItems[i][0] = menuItems[i][3] = data[0][i]
        else:
            menuItems[i] = data[0][i]
    data.pop(0)
    for i in range(len(msg)):
        msg[i] = data[i]

# Output settings
logging.basicConfig(format='[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.ERROR,
                    filename=os.path.join(os.path.dirname(__file__), os.path.join(iconPath, 'log.txt')))

def pasteClipboard():  # linux has a problem with pyperclip. Need to use the xclip. #sudo apt-get install xclip
    cb = subprocess.Popen('xclip -selection clipboard -out', shell=True, stdout=subprocess.PIPE)
    return cb.stdout.read().decode("utf-8")

def notification(title='',text='',execute='',icon=''):
   pass

def dlfolder():
    global dlpath
    try:
        if os.path.exists(os.path.join(dlpath,"settings.ini")):
            data = []
            f = open((os.path.join(dlpath,"settings.ini")), 'r')
            for s in f:
                data.append(s)
            f.close()
            dlpath = os.path.join(data[0], 'EasyDownloader')
            if not os.path.isdir(dlpath): os.mkdir(dlpath)
        else:
            dlpath = os.path.expanduser('~/Downloads')
            dlpath = os.path.join(dlpath, 'EasyDownloader')
            if not os.path.isdir(dlpath): os.mkdir(dlpath)
    except:
        dlpath = os.path.join(os.getcwd())
    return dlpath


if sys.platform == 'darwin':
    from mac_notification import notification

    ffmpegpath = os.path.join(ffmpegpath, "mffmpeg")
    traydl = 'traydl.png'
    tray = 'tray.png'
    ico = 'app.png' #icon for notification
    dlpath = dlfolder()
if sys.platform == 'win32':
    from win_notification import notification

    ffmpegpath = os.path.join(ffmpegpath, 'wffmpeg')
    dlpath = dlfolder()
    traydl = 'wintraydl.png'
    tray = 'wintray.png'
    ico = 'wintray.ico'
    fprog = 'start "" '  # open through exploler
if sys.platform == 'linux':
    from linux_notification import notification
    import subprocess
    pyperclip.paste = pasteClipboard
    traydl = 'wintraydl.png'
    tray = 'wintray.png'
    ico = ''
    ffmpegpath = '/usr/bin/ffmpeg'  #ffmpeg

ico = os.path.join(iconPath, ico) #make

if os.path.exists(os.path.join(iconPath, "lang.txt")): setlanguage(os.path.join(iconPath, "lang.txt"))

# download ffmpeg
if os.path.exists(ffmpegpath):
    if len(os.listdir(ffmpegpath)) == 0:
        notification(title=msg[5][0], text=msg[5][1], icon=ico)
        if dlffmpeg.dlffmpeg(ffmpegpath):
            notification(title=msg[7][0], text=msg[7][1], icon=ico)
        else:
            notification(title=msg[6][0], text=msg[6][1], icon=ico)
else:
    os.mkdir(ffmpegpath)
    notification(title=msg[5][0], text=msg[5][1], icon=ico)
    if dlffmpeg.dlffmpeg(ffmpegpath):
        notification(title=msg[7][0], text=msg[7][1], icon=ico)
    else:
        notification(title=msg[6][0], text=msg[6][1], icon=ico)


class Logger:
    def write(self, msg):
        logging.debug(msg)

    def flush(self):
        pass

#sys.stdout = Logger()

def complete(icon, status):
    global menuItems
    if menuItems[status][0] != menuItems[1]:
        menuItems[status][3] = menuItems[status][0]
        menuItems[status][2] = 1  # icon on btn
        menuItems[status][0] = menuItems[1]
        icon.icon = Image.open(os.path.join(iconPath, traydl))
    else:
        menuItems[status][2] = 0
        menuItems[status][0] = menuItems[status][3]
        m = 0
        for i in menuItems:
            if i[2] == 1: m = 1
        if m == 0: icon.icon = Image.open(os.path.join(iconPath, tray))
    icon.update_menu()


def predl(icon, opts, status, cb):
    try:
        fn = dl.dl(cb, ffmpegpath, opts, dlpath + fnMask)
        if fn == '':
            notification(title=msg[1][0], text=msg[1][1], execute=False, icon=ico)
        else:
            fn = fn[len(dlpath) + 1:]
            notification(title=msg[2][0], text=fn, execute="open " + dlpath + "/" + "'" + fn + "'", icon=ico)
        complete(icon, status)
    except Exception as e:
        logging.error(e)
        logging.error("cb = {0}".format(cb))
        notification(title=msg[3][0], text=msg[3][1], execute=False, icon=ico)
        complete(icon, status)


def on_clicked(icon, status, opts):
    global menuItems
    if menuItems[status][0] != menuItems[1]:  # cancel does not work
        complete(icon, status)

        cb = pyperclip.paste()

        # cb = 'https://www.youtube.com/watch?v=COwlqqErDbY'
        # cb = 'https://coub.com/view/1ade1p'
        error = dl.fastcheckcb(cb)
        if error == 0:
            Thread(target=predl, args=(icon, opts, status, cb)).start()
        else:
            complete(icon, status)
            notification(title=msg[0][0], text=msg[0][1],
                         execute=False, icon=ico)
    else:
        pass
        # Thread(target=restart, args=()).start()
        # rumps.quit_application()

def dlshow():
    global dlpath, fprog, msg
    if sys.platform == 'win32':
        os.system(fprog + '"{}"'.format(dlpath))

    notification(title=msg[4][0], text=dlpath, execute="open "+dlpath, icon=ico)


def close():
    icon.stop()

icon = Icon("name",
            Image.open(os.path.join(iconPath, tray)),
            "EasyDownloader",
            menu=menu(
                item(lambda title: menuItems[2][0], lambda icon: on_clicked(icon, 2, menuItems[2][1]),
                     checked=lambda item: menuItems[2][2]),
                item(lambda title: menuItems[3][0], lambda icon: on_clicked(icon, 3, menuItems[3][1]),
                     checked=lambda item: menuItems[3][2]),
                item(lambda title: menuItems[4][0], lambda icon: on_clicked(icon, 4, menuItems[4][1]),
                     checked=lambda item: menuItems[4][2]),
                menu.SEPARATOR,
                item(lambda title: menuItems[5], dlshow),
                menu.SEPARATOR,
                item(lambda title: menuItems[0], close)
            )
            )
icon.run()
