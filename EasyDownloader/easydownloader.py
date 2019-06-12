import os, pyperclip, dl, sys, logging
from PIL import Image
from pystray import Icon, Menu as menu, MenuItem as item
from threading import Thread



# sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'FilesDate'))

dlpath = iconPath = ffmpegpath = os.getcwdb().decode("utf-8")  # deafult ffmpeg path is folder with app
dlpath = ffmpegpath = iconPath = os.path.join(iconPath, 'data')
fnMask = '/%(title)s-%(id)s.%(ext)s'
menuItems = ['Quit', 'Cancel', ['Audio', 'mp3', 0, 'Audio'], ['Video', 'mp4', 0, 'Video'],
             ['Au+vi', 'mp4+mp3', 0, 'Au+vi'], 'Folder']
fprog = ''  # fix later

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
    if os.path.exists(os.path.join(dlpath,"settings.ini")):
        data = []
        f = open((os.path.join(dlpath,"settings.ini")), 'r')
        for s in f:
            data.append(s)
        f.close()
        dlpath = os.path.join(data[0], 'EasyDownloader')
    else:
        dlpath = os.path.expanduser('~/Downloads')
        dlpath = os.path.join(dlpath, 'EasyDownloader')
        if not os.path.isdir(dlpath): os.mkdir(dlpath)
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
    fprog = 'start '  # open through exploler
if sys.platform == 'linux':
    from linux_notification import notification
    import subprocess

    pyperclip.paste = pasteClipboard
    traydl = 'wintraydl.png'
    tray = 'wintray.png'
    ico = ''
    ffmpegpath = '/usr/bin/ffmpeg'  # program folder path for icons and ffmpeg

ico = os.path.join(iconPath, ico) #make


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
            notification(title='Error', text="Can't get file name. Check Donwloads folder", execute=False, icon=ico)
        else:
            fn = fn[len(dlpath) + 1:]
            notification(title='Download complete', text=fn, execute="open " + dlpath + "/" + "'" + fn + "'", icon=ico)
        complete(icon, status)
    except Exception as e:
        logging.error(e)
        logging.error("cb = {0}".format(cb))
        notification(title='Download error', text='The clipboard has a broken link', execute=False, icon=ico)
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
            notification(title='Download error', text='The clipboard does not have an youtube or coub link',
                         execute=False, icon = ico)
    else:
        pass
        # Thread(target=restart, args=()).start()
        # rumps.quit_application()

def dlshow():
    global dlpath, fprog
    os.system(fprog + dlpath)
    notification(title='Download folder', text=dlpath, execute="open "+dlpath, icon = ico)



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
