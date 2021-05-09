from .LogLevel import LogLevel
from .printer import ppprint


class Console:

    def log(self, message, tmp=False):
        return ppprint(message, LogLevel.LOG, tmp)

    def error(self, message, tmp=False):
        return ppprint(message, LogLevel.ERROR, tmp)

    def info(self, message, tmp=False):
        return ppprint(message, LogLevel.INFO, tmp)

    def debug(self, message, tmp=False):
        return ppprint(message, LogLevel.DEBUG, tmp)

    def warn(self, message, tmp=False):
        return ppprint(message, LogLevel.WARN, tmp)


console = Console()
