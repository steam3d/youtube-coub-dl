import pystray, os, pyperclip, dl, sys
from PIL import Image
from pystray import Icon, Menu as menu, MenuItem as item
from threading import Thread

dlPath =iconPath = ffmpegPath = os.getcwdb().decode("utf-8") #deafult ffmpeg path is folder with app
fnMask = '/%(title)s-%(id)s.%(ext)s'
menuItems = ['Quit','Cancel',['Audio','mp3',0,'Audio'],['Video','mp4',0,'Video'],['Au+vi','mp4+mp3',0,'Au+vi']]

def pasteClipboard(): #linux has a problem with pyperclip. Need to use the xclip. #sudo apt-get install xclip
    cb = subprocess.Popen('xclip -selection clipboard -out',shell=True,stdout = subprocess.PIPE)    
    return cb.stdout.read().decode("utf-8")

if sys.platform == 'darwin':
    from mac_notification import notification
    traydl = '/traydl.png'
    tray = '/tray.png'
    dlPath = os.path.expanduser('~/Downloads')
if sys.platform == 'win32':
    from win_notification import notification 
    traydl = '/wintraydl.png'
    tray = '/wintray.png'
if sys.platform == 'linux':
    from linux_notification import notification
    import subprocess
    pyperclip.paste = pasteClipboard
    traydl = '/wintraydl.png'
    tray = '/wintray.png'
    ffmpegPath = '/usr/bin/ffmpeg'   #program folder path for icons and ffmpeg

#def notification(title,text,execute):
#   pass
        
def complete(icon,status):
    global menuItems
    if  menuItems[status][0] != menuItems[1]:
        menuItems[status][3] = menuItems[status][0]
        menuItems[status][2] = 1 #icon on btn
        menuItems[status][0]= menuItems[1]
        icon.icon = Image.open(iconPath+traydl)      
    else:
        menuItems[status][2] = 0
        menuItems[status][0] = menuItems[status][3]
        m = 0
        for i in menuItems:
            if i[2] == 1: m = 1
        if m == 0: icon.icon = Image.open(iconPath+tray)
    icon.update_menu()

def predl(icon, opts, status, cb):
    try:
        fn = dl.dl(cb,ffmpegPath,opts,dlPath+fnMask)
        if fn == '':
            notification(title='Error',text = "Can't get file name. Check Donwloads folder", execute = False)    
        else:
            fn = fn[len(dlPath)+1:]
            notification(title='Download complete',text = fn, execute = "open "+dlPath+"/"+"'"+fn+"'")  
        complete(icon,status)
    except:
        notification(title='Download error',text = 'The clipboard has a broken link', execute = False)   
        complete(icon,status)
   
def on_clicked(icon,status,opts):
    global menuItems   
    if  menuItems[status][0] != menuItems[1]:#cancel does not work
        complete(icon,status)
        
        cb = pyperclip.paste()
        #cb = 'https://www.youtube.com/watch?v=COwlqqErDbY'
        #cb = 'https://coub.com/view/1ade1p'
        error = dl.fastcheckcb(cb)
        if error == 0:
            Thread(target=predl, args=(icon,opts,status,cb)).start()
        else:
            notification(title='Download error',text = 'The clipboard does not have an youtube or coub link', execute = False)
            complete(icon,status)
    else:
        pass
        #Thread(target=restart, args=()).start()
        #rumps.quit_application() 
    
def close():
    icon.stop()

icon = Icon("name",
            Image.open(iconPath+tray),
            "title",
            menu=menu(
                    item(lambda title: menuItems[2][0],lambda icon: on_clicked(icon,2,menuItems[2][1]),checked=lambda item: menuItems[2][2]),
                    item(lambda title: menuItems[3][0],lambda icon: on_clicked(icon,3,menuItems[3][1]),checked=lambda item: menuItems[3][2]),
                    item(lambda title: menuItems[4][0],lambda icon: on_clicked(icon,4,menuItems[4][1]),checked=lambda item: menuItems[4][2]),
                    menu.SEPARATOR,
                    item(lambda title: menuItems[0],close)
                    )
            )
icon.run()
