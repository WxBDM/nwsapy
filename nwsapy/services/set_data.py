"""Sets the data for the object. For every one NWSAPy object, there is one
function to set the data. The data that is being set will sometimes differ,
so sometimes it'll just be setting the iterable and returning the object.
Some instances it'll set each value from the request as an attribute.
"""

import copy

from ..endpoints.alerts import ActiveAlerts, AlertByArea, AlertById, AlertByMarineRegion, AlertByType, AlertByZone, AlertCount, Alerts, IndividualAlert, AlertById
from ..endpoints.glossary import Glossary
from ..endpoints.point import Point
from ..endpoints.server_ping import ServerPing

def nws_api_gave_error(response):
    """Checks to see if the API gave an error by checking to see if 
    ``correlationId`` is in the keys. There should be a more robust way
    to check to see if it's a bad API response.

    :param response: The response object from the ``requests`` module.
    :type response: requests.Response
    :return: True if it was a bad request, False otherwise.
    :rtype: bool
    """
    # There should be a more robust way of testing this.
    if 'correlationId' in list(response.keys()):
        return True
    
    return False

def __template(response):
    
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    # obj = Obj() 
    
    if nws_api_gave_error(response_values):
        # obj.values = response_values
        # obj.has_any_request_errors = True
        pass # <-- Remove this
    else:
        # Do whatever needs to get done.
        
        # obj.values = response_values
        # Could also set as attributes, depending upon the object.
        # for key, value in response_values.items():
        #     setattr(ping, key, value)
        pass # <-- Remove this
    
    # obj.response_headers = response_headers
    # obj._set_iterator()
    #
    # return obj

def _change_from_camel_case(word):
    """Changes dictionary values from camelCase to camel_case.
    This is done so that attributes of the object are more
    python-like.

    :param word: A string of a word to convert
    :type word: string
    :return: A string of the converted word from camelCase to camel_case
    :rtype: string
    """
    return_word = ''
    for letter in word:
        if letter.isupper():
            letter = f'_{letter.lower()}'
        return_word += letter
    return return_word

def for_server_ping(response):
    
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    ping = ServerPing()
    
    if nws_api_gave_error(response_values):
        ping.values = response_values
        ping.has_any_request_errors = True
    else:
        ping.values = response_values
        
        for key, value in response_values.items():
            setattr(ping, key, value)

    
    ping.values = response_values
    ping.response_headers = response_headers
    ping._set_iterator()
    
    return ping

def for_glossary(response):
    
    # unpack response
    response_values, response_headers = response
    
    # instantiate object
    glossary = Glossary()
    
    if nws_api_gave_error(response_values):
        glossary.values = response_values
        glossary.has_any_request_errors = True
    else:
        # iterate through the response and set the key/value pairs, then set
        # it into a `values` variable. This is then set into the glossary object.
        values = {}
        for element in response_values['glossary']:
            term = element['term']
            definition = element['definition']
            values[term] = definition
            
            # not setting them as attributes because it won't make sense. There's
            #   spaces, and it would be weird (i.e. glossary.zulu), lots of
            #   individual handling = lots of dev time = maticulus work.
    
        glossary.values = values
        
    glossary.response_headers = response_headers
    glossary._set_iterator()
    
    return glossary

def for_point(response):
    
    # unpack response
    response_values, response_headers = response
    
    point = Point()
    
    if nws_api_gave_error(response_values):
        point.values = response_values
        point.has_any_request_errors = True
    else:
        # TODO: Look into handling this. If this not in the response,
        # then it is beyond NWSAPy. How does the package handle?
        values = response_values['properties']
        
        values['id'] = values['@id']

        values['forecast_zone_url'] = values['forecastZone']
        values['forecast_zone'] = values['forecastZone'].split("/")[-1]

        values['county_url'] = values['county']
        values['county'] = values['county'].split("/")[-1]

        values['fire_weather_zone_url'] = values['fireWeatherZone']
        values['fire_weather_zone'] = values['fireWeatherZone'].split("/")[-1]

        rloc_props = values['relativeLocation']['properties']
        values['city'] = rloc_props['city']
        values['state'] = rloc_props['state']
        values['bearing'] = rloc_props['bearing']
        values['distance'] = rloc_props['distance']
        values['state'] = rloc_props['state']

        # Set each value as an attribute. Also get rid of some information, but
        # all original values can be accesed through obj.values or obj['values'].
        # Also, get rid of camelCase. Who does this anyways?
        values_to_set = copy.deepcopy(values) # make a deep copy
        del values_to_set['@id']
        del values_to_set['@type']
        del values_to_set['relativeLocation']

        for k, v in values_to_set.items():
            k = _change_from_camel_case(k)
            setattr(point, k, v)
        
        # Set the iterable object
        point.values = values

    point.response_headers = response_headers
    point._set_iterator()
    
    return point

def for_alerts(response):
    
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint
    alerts = Alerts()
    
    if nws_api_gave_error(response_values):
        alerts.values = response_values
        alerts.has_any_request_errors = True
    else:
        alerts.values = [IndividualAlert(x) for x in response_values['features']]
    
    alerts.response_headers = response_headers
    alerts._set_iterator()
    return alerts

def for_active_alerts(response):
    
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    alerts = ActiveAlerts()
    
    if nws_api_gave_error(response_values):
        alerts.values = response_values
        alerts.has_any_request_errors = True
    else:
        alerts.values = [IndividualAlert(x) for x in response_values['features']]
    
    alerts.response_headers = response_headers
    alerts._set_iterator()
    return alerts

def for_alert_by_id(response):
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    alerts = AlertById()
    
    if nws_api_gave_error(response_values):
        alerts.values = response_values
        alerts.has_any_request_errors = True
    else:
        alerts.values = [IndividualAlert(response_values)]

    alerts.response_headers = response_headers
    alerts._set_iterator()
    return alerts

def for_alert_by_area(response):
    
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    alert = AlertByArea() 
    
    if nws_api_gave_error(response_values):
        alert.values = response_values
        alert.has_any_request_errors = True
    else:
        features = response_values['features']
        alert.values = [IndividualAlert(x) for x in features]

    alert.response_headers = response_headers
    alert._set_iterator()
    return alert

def for_alert_count(response):
    
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    count = AlertCount()
    
    if nws_api_gave_error(response_values):
        count.values = response_values
        count.has_any_request_errors = True
    else:
        # Do whatever needs to get done.
        values = {
            'total' : response_values['total'],
            'land' : response_values['land'],
            'marine' : response_values['marine'],
            'regions' : response_values['regions'],
            'areas' : response_values['areas'],
            'zones' : response_values['zones']
        }
        
        count.values = values
    
    count.response_headers = response_headers
    count._set_iterator()
    return count

def for_alert_by_zone(response):
        
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    alert = AlertByZone() 
    
    if nws_api_gave_error(response_values):
        alert.values = response_values
        alert.has_any_request_errors = True
    else:
        features = response_values['features']
        alert.values = [IndividualAlert(x) for x in features]
    
    alert.response_headers = response_headers
    alert._set_iterator()
    return alert

def for_alert_by_marine_region(response):
        
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    alert = AlertByMarineRegion() 
    
    if nws_api_gave_error(response_values):
        alert.values = response_values
        alert.has_any_request_errors = True
    else:
        features = response_values['features']
        alert.values = [IndividualAlert(x) for x in features]
    
    alert.response_headers = response_headers
    alert._set_iterator()
    return alert

def for_alert_type(response):
        
    # unpack
    response_values, response_headers = response
    
    # Instantiate endpoint (remember to import)
    alert = AlertByType() 
    
    if nws_api_gave_error(response_values):
        alert.values = response_values
        alert.has_any_request_errors = True
    else:
        alert.values = response_values['eventTypes']
    
    alert.response_headers = response_headers
    alert._set_iterator()
    return alert