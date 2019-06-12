import pync

def notification(title,text,execute=False, icon=''):
    text = text.replace('[','')
    text = text.replace(']','')

    if execute == False:
        pync.notify(text, title=title)
    else:
        pync.notify(text, title=title, execute=execute, appIcon=icon)