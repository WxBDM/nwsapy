_config = {
    'showTime': True,
    'showLvl': True
}


def setConfig(key, val):
    _config[key] = val


def getConfig(key=None):
    try:
        return _config[key]
    except KeyError:
        return _config
