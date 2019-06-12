import pync

def notification(title,text,execute=False):
    text = text.replace('[','')
    text = text.replace(']','')
    if execute == False:
        pync.notify(text, title=title)
    else:
        pync.notify(text, title=title, execute=execute)