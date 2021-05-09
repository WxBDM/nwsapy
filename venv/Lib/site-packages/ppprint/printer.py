import sys
from datetime import datetime

from .LogLevel import LogLevel
from .config import getConfig
from .colorize import colorize
from .lvlColor import getLvlColor


def ppprint(message, lvl=LogLevel.LOG, tmp=False):
    """[summary]

    Args:
        message (str): [description]
        lvl (LogLevel, optional): Classic log level. Defaults to LogLevel.LOG.
        progress (float, optional): Shows a progress % if >0. Defaults to 0.0.
        tmp (bool, optional): Temporary message will be erased. Defaults to False.
    """

    timestamp = ''
    level = ''
    prgrs = ''

    if getConfig('showTime'):
        timestamp = str(datetime.now())

    if getConfig('showLvl'):
        level = colorize("[{}]".format(lvl.name[0]), getLvlColor(lvl))

    msg = ' '.join([timestamp, level, message])
    if tmp:
        print(msg, end="\r")
    else:
        print(msg)
