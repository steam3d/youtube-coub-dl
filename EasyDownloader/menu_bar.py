import pync, os, pyperclip, dl, sys
from threading import Thread
from rumps import *
menu = [['Working',0],['Audio',0],['Video',0],['Au+vi',0]]
path = '~/Downloads'
ffmpegPath = os.getcwdb().decode("utf-8")   #program folder path for icons and ffmpeg
os.chdir(os.path.expanduser(path)) #download folder path

def predl(opts,file_type,sender,self,status):
    cb = pyperclip.paste() 
    if cb == None: cb='None'
    fn = dl.dl(cb,ffmpegPath,opts)
    if fn == '':
        pync.notify('Clipboard does not have an youtube link', title='Download error')
    else:
        loop = 0
        while (fn[-1:] != '.') and (loop !=10):
            fn = fn[:-1]
            loop = loop+1
        if loop == 10:
            pync.notify("Can't get file name. Check Donwloads folder", title='Error')
        else:
            pync.notify(fn+file_type, title='Download complete',execute="open "+path+"/"+"'"+fn+file_type+"'")
    sender.title = sender.btn
    sender.state = 0
    menu[status][1] = 0
    m = 0
    for i in menu:
        if i[1] == 1: m = 1
    if m == 0: self.icon = ffmpegPath+'/tray.png'
    
def start(self,sender,status,opts,file_type):
    if sender.title != menu[0][0]:#cancel does not work
        sender.btn = sender.title
        sender.title= menu[0][0]
        self.icon = ffmpegPath+'/traydl.png'
        menu[status][1] = 1
        Thread(target=predl, args=(opts,file_type,sender,self,status)).start()
        sender.state = 1

class AwesomeStatusBarApp(rumps.App):
    @rumps.clicked(menu[1][0])
    def prefs1(self,sender):
        start(self,sender,1,'mp3','mp3')

    @clicked(menu[2][0])
    def prefs2(self,sender):
        start(self,sender,2,'mp4','mp4')

    @clicked(menu[3][0])
    def prefs3(self,sender):
        if (pyperclip.paste() != None): #Coub does not support Audio + video
            if ('https://coub.com/' in pyperclip.paste()):
                pync.notify("Coub does not support "+menu[3][0], title='Error')
            else:
                start(self,sender,3,'mp4+mp3','mp4')

if __name__ == "__main__":
    AwesomeStatusBarApp("Easy Downloader",icon=ffmpegPath+'/tray.png').run()

