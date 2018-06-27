import pync, os, pyperclip, dl, sys
from threading import Thread
from rumps import *

menu = [['Cancel',0],['Audio',0],['Video',0],['Au+vi',0]]
path = '~/Downloads'
ffmpegPath = os.getcwdb().decode("utf-8")   #program folder path for icons and ffmpeg
os.chdir(os.path.expanduser(path)) #download folder path

def complete(self,sender,status):
    if sender.title != menu[0][0]:
        sender.btn = sender.title
        sender.state = 1
        sender.title= menu[0][0]
        menu[status][1] = 1
        self.icon = ffmpegPath+'/traydl.png'      
    else:
        sender.state = 0
        sender.title = sender.btn
        menu[status][1] = 0
        m = 0
        for i in menu:
            if i[1] == 1: m = 1
        if m == 0: self.icon = ffmpegPath+'/tray.png'

def restart(): #Try not to use it
    os.system('open -a "Easy Downloader"')

def predl(opts,sender,self,status,cb):
    try:
        fn = dl.dl(cb,ffmpegPath,opts)
        if fn == '':
            pync.notify("Can't get file name. Check Donwloads folder", title='Error')        
        else:
            pync.notify(fn, title='Download complete',execute="open "+path+"/"+"'"+fn+"'")
        complete(self,sender,status)
    except:
        pync.notify('The clipboard has a broken link', title='Download error')
        complete(self,sender,status)
   
def start(self,sender,status,opts):
    if sender.title != menu[0][0]:#cancel does not work
        complete(self,sender,status)
        
        cb = pyperclip.paste()
        error = dl.fastcheckcb(cb)
        
        if error == 0:
            Thread(target=predl, args=(opts,sender,self,status,cb)).start()
        else:
            pync.notify('The clipboard does not have an youtube or coub link', title='Download error')
            complete(self,sender,status)
    else:
        Thread(target=restart, args=()).start()
        rumps.quit_application()        

class AwesomeStatusBarApp(rumps.App):
    @rumps.clicked(menu[1][0])
    def prefs1(self,sender):
        start(self,sender,1,'mp3')

    @clicked(menu[2][0])
    def prefs2(self,sender):
        start(self,sender,2,'mp4')

    @clicked(menu[3][0])
    def prefs3(self,sender):
        if (pyperclip.paste() != None): #Coub does not support Audio + video
            if ('https://coub.com/' in pyperclip.paste()):
                pync.notify("Coub does not support "+menu[3][0], title='Error')
            else:
                start(self,sender,3,'mp4+mp3')

if __name__ == "__main__":
    AwesomeStatusBarApp("Easy Downloader",icon=ffmpegPath+'/tray.png').run()
