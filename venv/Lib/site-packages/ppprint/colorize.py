from .Color import Color


def _colorTag(colorNum):
    if colorNum == None:
        colorNum = 0
    return '\x9B' + str(colorNum) + 'm'


def colorize(message, color, bright=False, background=False):
    """Returns a colorized message, according to arguments.

    Args:
        message (str): Message to colorize.
        color (Color): Chosen color from Color enum.
        bright (bool, optional): Use bright-version of color. Defaults to False.
        background (bool, optional): Apply color to background instead of font. Defaults to False.

    Returns:
        str: Colorized message
    """
    if background:
        color += Color.BACKGROUND
    if bright:
        color += Color.BRIGHT

    return _colorTag(color.value) + message + _colorTag(None)
