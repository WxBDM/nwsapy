from .LogLevel import LogLevel
from .Color import Color

_lvlColor = {}
_lvlColor[LogLevel.ERROR.name] = Color.RED
_lvlColor[LogLevel.WARN.name] = Color.YELLOW
_lvlColor[LogLevel.INFO.name] = Color.GREEN
_lvlColor[LogLevel.LOG.name] = Color.NONE
_lvlColor[LogLevel.DEBUG.name] = Color.CYAN


def setLvlColor(lvl, color):
    """Assign a color to a log level

    Args:
        lvl (LogLevel): Log level
        color (Color): Color
    """
    _lvlColor[lvl.name] = color


def getLvlColor(lvl=None):
    """Get the color assigned to a level. If no key is used, fallback to complete mapping.

    Args:
        lvl (LogLevel, optional): [description].

    Returns:
        Color: the color assigned to the log level
    """
    try:
        return _lvlColor[lvl.name]
    except (KeyError, AttributeError):
        return _lvlColor
