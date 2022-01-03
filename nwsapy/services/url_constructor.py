def construct_alert_url(params, is_active_alerts = True):
    
    # Weird logic going on here, but the values need to be iterable, so if
    #   it's just a string, it'll be put into a list.
    #   This just formats the data so that when it goes into data validation
    #   it will already be formatted. Maybe refactor this into the data validation
    #   part? Currently, data validation happens as a single element in the list.
    
    # Note: the keys are guarenteed to be in the params dict.
    if is_active_alerts:
        url = "https://api.weather.gov/alerts/active"
    else:
        url = "https://api.weather.gov/alerts"
        
    url_appendage = []
    for key, value in params.items():
        # another method: just assume that it's a string. More risky this way
        # though in terms of errors.
        if not any([isinstance(value, list), isinstance(value, tuple)]):
            value = [value]
        
        if len(value) == 1:
            url_appendage.append(f'{key}={value[0]}')
        else:
            url_appendage.append(f"{key}={','.join(value)}")
        
    url_appendage = "&".join(url_appendage)
    url = "?".join([url, url_appendage]).replace(' ', "%20")
    return url