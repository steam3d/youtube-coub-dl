import os
import pyperclip
import dl
import sys
import logging
import subprocess
import dlffmpeg
import tempfile
import shutil  # for move files
import psutil  # for kill ffmpeg process

from exceptions import TerminateThreadException
from datetime import datetime
from PIL import Image
from pystray import Icon, Menu as menu, MenuItem as item
from threading import Thread


class ProxySubprocessPopen(subprocess.Popen):  # Fix showing console on windows

    if sys.platform == "win32":
        # noinspection PyUnresolvedReferences
        def _execute_child(self, args, executable, preexec_fn, close_fds,
                           cwd, env, universal_newlines,
                           startupinfo, *kwargs):
            if startupinfo is None:
                startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = 1
            startupinfo.wShowWindow = 0
            super(ProxySubprocessPopen, self)._execute_child(args, executable, preexec_fn, close_fds,
                                                             cwd, env, universal_newlines,
                                                             startupinfo, *kwargs)


subprocess.Popen = ProxySubprocessPopen

dlpath = ffmpegpath = iconPath = os.path.join(os.getcwd(), 'data')  # default path for all contents
fnmask = '/%(title)s-%(id)s.%(ext)s'  # file name mask for youtube-dl
fprog = ''  # fix later
add_to_opts = {'noplaylist': True}
signals = {}  # destroy treads. False does not destroy, True destroy.

menu_items = ['Quit', 'Cancel', ['Only Audio', 'mp3', 0, 'Only Audio'], ['Only Video', 'mp4', 0, 'Only Video'],
              ['Audio+Video', 'mp4+mp3', 0, 'Audio+Video'], 'Show downloads', ['Download playlist', 0]]
# for languages
msg = [['Download error', 'The clipboard does not have a link'],
       ['Error', "Can't get file name. Check Donwloads folder"],
       ['Download complete', ''],
       ['Download error', 'The clipboard has a broken link'],
       ['Canceled download', ''],
       ['Downloading ffmpeg', 'Please wait until the download is complete'],
       ['Downloading error', 'Something went wrong'],
       ['Download complete', 'Running the app']]


def setlanguage(p):
    global menu_items, msg
    with open(p, 'r',  encoding="utf-8") as f:
        data = f.readlines()
        data = [line.rstrip() for line in data]
        data = [line.split(';') for line in data]
    for i in range(len(menu_items)):
        if type(menu_items[i]) is list:
            #menuItems[i][0] = menuItems[i][3] = data[0][i]
            menu_items[i][0] = data[0][i]
        else:
            menu_items[i] = data[0][i]
    data.pop(0)
    for i in range(len(msg)):
        msg[i] = data[i]


# log
logging.basicConfig(format='[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.ERROR,
                    filename=os.path.join(os.path.dirname(__file__), os.path.join(iconPath, 'log.txt')))


def pasteclipboard():  # linux has a problem with pyperclip. Need to use the xclip. #sudo apt-get install xclip
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
    pyperclip.paste = pasteclipboard
    traydl = 'wintraydl.png'
    tray = 'wintray.png'
    ico = ''
    ffmpegpath = '/usr/bin/ffmpeg'  #ffmpeg

ico = os.path.join(iconPath, ico)  # set notification icon

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
    global menu_items
    if menu_items[status][0] != menu_items[1]:
        menu_items[status][3] = menu_items[status][0]
        menu_items[status][2] = 1  # icon on btn
        menu_items[status][0] = menu_items[1]
        icon.icon = Image.open(os.path.join(iconPath, traydl))
    else:
        menu_items[status][2] = 0
        menu_items[status][0] = menu_items[status][3]
        m = 0

        for i in menu_items:
            if len(i) == 4:
                if i[2] == 1: m = 1
        if m == 0: icon.icon = Image.open(os.path.join(iconPath, tray))
    icon.update_menu()


def movefiles(src, dst, plstdir):
    # copy from src to dst
    # plstdir for playlist dir name
    result = []
    ignore_list = ['.DS_Store']

    for addr, folders, files in os.walk(src):
        for i in ignore_list:
            if i in files: files.remove(i)

        if len(files) > 0:  # forder empty or not
            if len(files) > 1:
                dst = os.path.join(dst, os.path.basename(plstdir))
                if not os.path.exists(dst):
                    os.mkdir(dst)
                else:
                    dst += datetime.today().strftime('_%Y-%m-%d_%H-%M-%S')
                    os.mkdir(dst)
                result = ['playlist', dst]

            for f in files:
                # if file already exist we must rename current file to unique
                if not os.path.isfile(os.path.join(dst, f)):
                    shutil.move(os.path.join(src, f), dst)
                    pass
                else:
                    ext = f.rfind('.')  # .mp3 extension of file can be more than 4 symbols + 1 dot
                    if (ext != - 1) and (len(f) - ext <= 5):
                        old_f = f  # old name of file
                        f = f[:ext] + datetime.today().strftime('_%Y-%m-%d_%H-%M-%S') + f[ext:]
                        os.rename(os.path.join(src, old_f), os.path.join(src, f))
                    else:
                        f = f + datetime.today().strftime('_%Y-%m-%d_%H-%M-%S')  # if can't find ext, just add date
                    shutil.move(os.path.join(src, f), dst)
            if result == []: result = ['file', os.path.join(dst, f)]
        break

    if result == []: result = ['error', '']
    return result


def terminate_thread(pid):
    for proc in psutil.process_iter():
        try:
            tmp = proc.as_dict(attrs=['pid', 'ppid', 'name', 'username'])
            if tmp['ppid'] == pid:
                if 'ffmpeg' in tmp['name']:  # Can it  be other process?
                    p_kill = psutil.Process(tmp['pid'])
                    p_kill.terminate()
                    logging.debug('pid = {0}, ppid = {1} killed'.format(tmp['pid'], tmp['ppid']))
        except psutil.NoSuchProcess as e:
            logging.error(e)


def predl(icon, opts, status, cb):
    global add_to_opts, ico, signals, dlpath

    with tempfile.TemporaryDirectory() as tmpdirpath:
        try:
            fn = dl.dl(cb, ffmpegpath, opts, tmpdirpath + fnmask, signals[status], add_to_opts)
            result = movefiles(tmpdirpath, dlpath, fn)
            if result[0] == 'file':
                notification(title=msg[2][0], text=os.path.basename(result[1]), execute="open " + "'" + result[1] + "'",
                             icon=ico)
            else:
                if result[0] == 'playlist':
                    notification(title=msg[2][0], text=os.path.basename(result[1]), execute="open " + "'" + result[1] + "'", icon=ico)
                else:  # if error
                    notification(title=msg[1][0], text=msg[1][1], execute=False, icon=ico)

            complete(icon, status)

        except Exception as e:
            if signals[status][0] == True:
                notification(title=msg[4][0], text=cb, execute=False, icon=ico)
                complete(icon, status)
            else:
                logging.error(e)
                logging.error("cb = {0}".format(cb))
                notification(title=msg[3][0], text=msg[3][1], execute=False, icon=ico)
                complete(icon, status)

        # except TerminateThreadException as e: # does not catch now


def on_clicked(icon, status, opts):
    global menu_items, signals
    if menu_items[status][0] != menu_items[1]:  # cancel does not work
        complete(icon, status)

        cb = pyperclip.paste()

        # cb = 'https://youtu.be/plv1gcRcix8'
        # cb = 'https://www.youtube.com/watch?v=COwlqqErDbY'
        # cb = 'https://coub.com/view/1ade1p'
        if dl.isurl(cb):
            signals[status] = [False]  # cuz
            t = Thread(target=predl, args=(icon, opts, status, cb))
            t.daemon = True
            t.start()
        else:
            complete(icon, status)
            notification(title=msg[0][0], text=msg[0][1],
                         execute=False, icon=ico)
    else:
        signals[status][0] = True
        terminate_thread(os.getpid())


def dlshow():
    global dlpath, fprog, msg
    if sys.platform == 'win32':
        subprocess.Popen('explorer "%s"'%(dlpath), shell=True)
    else:
        notification(title='Downloads folder', text=dlpath, execute="open " + dlpath, icon=ico)
        #os.system('open "%s"'%(dlpath))
        #subprocess.Popen('open "%s"'%(dlpath), shell=True)


def dlplst(icon,status):
    global menu_items, add_to_opts
    if menu_items[status][1] == 0:
        menu_items[status][1] = 1
        add_to_opts.update({'noplaylist': False})
    else:
        menu_items[status][1] = 0
        add_to_opts.update({'noplaylist': True})
    icon.update_menu()


def close():
    icon.stop()


icon = Icon("name",
            Image.open(os.path.join(iconPath, tray)),
            "EasyDownloader",
            menu=menu(
                item(lambda title: menu_items[2][0], lambda icon: on_clicked(icon, 2, menu_items[2][1]),
                     checked=lambda item: menu_items[2][2]),
                item(lambda title: menu_items[3][0], lambda icon: on_clicked(icon, 3, menu_items[3][1]),
                     checked=lambda item: menu_items[3][2]),
                item(lambda title: menu_items[4][0], lambda icon: on_clicked(icon, 4, menu_items[4][1]),
                     checked=lambda item: menu_items[4][2], default=True),
                menu.SEPARATOR,
                item(lambda title: menu_items[6][0], lambda icon: dlplst(icon, 6),
                     checked=lambda item: menu_items[6][1]),
                item(lambda title: menu_items[5], dlshow),
                menu.SEPARATOR,
                item(lambda title: menu_items[0], close)
            )
            )
icon.HAS_DEFAULT_ACTION = True

if __name__ == '__main__':
    icon.run()
