import pync

def notification(title,text,execute):
    if execute == False:
        pync.notify(text, title=title)
    else:
        pync.notify(text, title=title, execute=execute)
