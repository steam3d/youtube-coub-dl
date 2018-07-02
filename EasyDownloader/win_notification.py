import time
from win10toast import ToastNotifier
toaster = ToastNotifier()
def notification(text,title, execute):
    #toaster = ToastNotifier()
    toaster.show_toast(title, text,#icon_path="custom.ico",
                       duration=10,
                       threaded=True)
    # Wait for threaded notification to finish
    #while toaster.notification_active(): time.sleep(0.1)
