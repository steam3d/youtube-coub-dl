class TerminateThreadException(Exception):
    def __init__(self, info, error):
        self.info = info
        self.error = error