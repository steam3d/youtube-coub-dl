from __future__ import unicode_literals
import youtube_dl
import os

msg = ''


def prnt(msg):
    pass
    #print(bytes(msg, 'utf-8'))


from exceptions import TerminateThreadException


def isurl(cb):
    # if cb == None: cb = 'None' idk fow what
    if ('https://' in cb) or ('http://' in cb): return True
    return False


def coubfix(fn):  # Fix for coub video
    with open(fn,'rb') as f:
        data = f.read()
    with open(fn, 'wb') as f:
        f.write(b'\x00\x00' + data[2:])


def dl(cb, ffmpegpath, opts, dlpath, signal=[False], add_to_opts=None):
    fn = ''  # file name from download URL

    class MyLogger(object):
        def __init__(self, signal):
            self.signal = signal

        def debug(self, msg):
            if self.signal[0] == True:
                raise TerminateThreadException('Exit', 'Thread was killed')
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
                'outtmpl': dlpath,
                'forcefilename': False,
                'ffmpeg_location': ffmpegpath,
                'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                 }],
                 'logger': MyLogger(signal),
                 'progress_hooks': [my_hook],
                 },
        'mp4': {'nocheckcertificate': True,
                'outtmpl': dlpath,
                'ffmpeg_location': ffmpegpath,
                'forcefilename': True,
                'format': 'bestvideo/best',
                'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat':'mp4'
                }],
                'logger': MyLogger(signal),
                'progress_hooks': [my_hook],
                },
        'mp4+mp3': {'nocheckcertificate': True,
                'outtmpl': dlpath,
                'ffmpeg_location': ffmpegpath,
                'forcefilename': True,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'logger': MyLogger(signal),
                'progress_hooks': [my_hook],
                }
        }
    if add_to_opts != None:
        if type(add_to_opts) == dict:
            options[opts].update(add_to_opts)

    if isurl(cb):
        with youtube_dl.YoutubeDL(options[opts]) as ydl:
            ydl.download([cb])
            info_dict = ydl.extract_info(cb, download=False)
            fn = ydl.prepare_filename(info_dict)

        if ('https://coub.com/' in cb) and ('mp4' in opts): coubfix(fn)
    return fn


if __name__ == "__main__":
    ffmpegpath = os.getcwdb().decode("utf-8")
    dlPath = ffmpegpath + '/%(title)s-%(id)s.%(ext)s'

    cb = 'https://www.youtube.com/watch?v=zZohSJyYknY'
    print(dl(cb, ffmpegpath, 'mp4+mp3', dlPath))

    cb = 'https://coub.com/view/1aa6m1'
    print(dl(cb, ffmpegpath, 'mp4', dlPath))


