import requests
from requests.exceptions import HTTPError


def request_from_api(url, headers):
    # requests a url. For this purpose, this should be a NWS API url.
    # list of URLs: https://www.weather.gov/documentation/services-web-api#/

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError:
        # Possible error message: requests.exceptions.HTTPError: 503 Server Error:
        #   Service Unavailable for url: https://api.weather.gov/alerts/active
        return response
    except Exception as err:
        raise Exception(f'Other error occurred: {err}')

    return response