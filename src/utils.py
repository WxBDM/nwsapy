"""Utility file."""

import requests
from requests.exceptions import HTTPError


def request(url):
    # requests a url. For this purpose, this should be a NWS API url.
    # list of URLs: https://www.weather.gov/documentation/services-web-api#/

    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError:
        query = response.json()
        query.update({'event' : 'error'})
        error_obj = type(query['title'].replace(" ", "").lower(), (), query)
        return error_obj()
    except Exception as err:
        raise Exception(f'Other error occurred: {err}')

    return response
