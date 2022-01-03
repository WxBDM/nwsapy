import requests
from requests import HTTPError

def request_from_api(url, headers, as_response_object = False):
    """Requests data from the NWS API and returns a response.

    :param url: The URL to request from.
    :type url: str
    :param headers: The headers to include in the response.
    :type headers: dict
    :raises Exception: If a bad request is made, raise an exception.
    :return: A response from the NWS API.
    :rtype: requests.Response
    """
    # requests a url. For this purpose, this should be a NWS API url.
    # list of URLs: https://www.weather.gov/documentation/services-web-api#/

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError:
        # Possible error message: requests.exceptions.HTTPError: 503 Server Error:
        #   Service Unavailable for url: https://api.weather.gov/alerts/active
        if as_response_object:
            return response
        
        return (response.json(), response.headers)
    except Exception as err:
        raise Exception(f'Other error occurred: {err}')

    # Return this as a tuple with the headers and as a dictionary. This will
    #   help with testing and end-to-end data flow.
    if as_response_object:
        return response
    
    return (response.json(), response.headers)