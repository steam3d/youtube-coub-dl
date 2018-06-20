from __future__ import unicode_literals
import youtube_dl, os, time

msg = ''
def prnt (msg):
    pass
    #print(bytes(msg, 'utf-8'))

def coubFix(fn): #Fix for coub video
    path = os.getcwd() + '/' + fn #dangerous decision
    with open(path,'rb') as f:
        data = f.read()
    with open(path, 'wb') as f:
        f.write(b'\x00\x00' + data[2:])

def dl(cb,ffmpegPath,opts):
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
                'ffmpeg_location': ffmpegPath,
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
                'ffmpeg_location': ffmpegPath,
                'format': 'bestvideo/best',
                'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat':'mp4'
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
                },
        'mp4+mp3': {'nocheckcertificate': True,
                'ffmpeg_location': ffmpegPath,
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
    if ('https://coub.com/' in cb) and ('mp4' in opts): coubFix(fn) 
    return fn
