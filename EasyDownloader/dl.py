from __future__ import unicode_literals
import youtube_dl, os

msg = ''
def prnt (msg):
    pass
    #print(bytes(msg, 'utf-8'))

def fastcheckcb(cb):
    if cb == None: cb='None'
    if ('https://youtu.be/' in cb) or ('https://www.youtube.com/' in cb) or ('https://coub.com/' in cb):
        error = 0
    else:
        error = 1
    return error

def coubFix(fn): #Fix for coub video
    path = os.getcwd() + '/' + fn #dangerous decision
    with open(path,'rb') as f:
        data = f.read()
    with open(path, 'wb') as f:
        f.write(b'\x00\x00' + data[2:])

def dl(cb,ffmpegPath,opts,dlPath):
    fn=''
    class MyLogger(object):
        def debug(self, msg):
            prnt(msg)

        def warning(self, msg):
            prnt(msg)

        def error(self, msg):
            prnt(msg)

    def my_hook(d):
            pass
            #if d['status'] == 'finished':
            #    msg = 'Done downloading, now converting ...'
            #    prnt(msg)

    options = {
        'mp3': {'nocheckcertificate': True,
                'outtmpl': dlPath,
                'ffmpeg_location': ffmpegPath,
                'forcefilename': True, 
                'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                 }],
                 'logger': MyLogger(),
                 'progress_hooks': [my_hook],
                 },
        'mp4': {'nocheckcertificate': True,
                'outtmpl': dlPath,                
                'ffmpeg_location': ffmpegPath,
                'forcefilename': True, 
                'format': 'bestvideo/best',
                'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat':'mp4'
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
                },
        'mp4+mp3': {'nocheckcertificate': True,
                'outtmpl': dlPath,
                'ffmpeg_location': ffmpegPath,
                'forcefilename': True,   
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
                }
        }
    
    if ('https://youtu.be/' in cb) or ('https://www.youtube.com/' in cb) or ('https://coub.com/' in cb):
    
        with youtube_dl.YoutubeDL(options[opts]) as ydl:
            ydl.download([cb])
            info_dict = ydl.extract_info(cb, download=False)
            fn = ydl.prepare_filename(info_dict)
            loop = 0
            while (fn[-1:] != '.') and (loop !=10):
                fn = fn[:-1]
                loop = loop+1
            if loop == 10:
                fn = ''
            else:
                if opts == 'mp3':
                    fn = fn + 'mp3'
                else:
                    fn = fn + 'mp4'    
    if ('https://coub.com/' in cb) and ('mp4' in opts): coubFix(fn)
    return fn

if __name__ == "__main__":
    dlPath = '/Users/steam3d/Downloads/%(title)s-%(id)s.%(ext)s'
    ffmpegPath = os.getcwdb().decode("utf-8")
    cb = 'https://www.youtube.com/watch?v=zZohSJyYknY'
    print(dl(cb,ffmpegPath,'mp4+mp3',dlPath))
    print(dl(cb,ffmpegPath,'mp4+mp3',dlPath))

