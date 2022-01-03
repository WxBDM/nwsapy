"""Utility file."""
import copy
import json
import requests
from requests.exceptions import HTTPError
import pandas as pd


class ErrorObject:
    # Can't put docstring here, sphinx won't recognize it >:(
    def __init__(self, response):
        response = json.loads(response.text)
        for k, v in response.items():  # the response text is going to allow us to see the response from the API
            setattr(self, k, v)

<<<<<<< HEAD:nwsapy/utils.py
    def __repr__(self):
        msg = f"Error details:\nStatus: {self.status}\nDescription: {self.detail}\nCorrelation ID: {self.correlationId}" \
              f"Instance: {self.instance}\nType: {self.type}"
        return msg
=======
        self._d = response

    def to_dict(self):
        return self._d

    def to_dataframe(self):
        s = pd.Series(data = self._d)
        return pd.DataFrame(s).transpose() # transpose it so columns are named the attributes.
>>>>>>> rewrite:old_package/utils.py


class ObjectIterator:

    def __iter__(self):
        """Allows for iteration though object."""
        self._index = 0
        return self

    def __next__(self):
        """Allows for iteration through object."""
        if self._index < len(self._iterable):
            val = self._iterable[self._index]
            self._index += 1
            return val
        else:
            raise StopIteration

    def __getitem__(self, index):
        """Allows for object to be directly indexable."""
        return self._iterable[index]

    def __len__(self):
        return len(self._iterable)


def request(url, headers):
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


def valid_products():
    return ['911 Telephone Outage Emergency', 'Administrative Message', 'Air Quality Alert', 'Air Stagnation Advisory',
            'Arroyo And Small Stream Flood Advisory', 'Ashfall Advisory', 'Ashfall Warning', 'Avalanche Advisory',
            'Avalanche Warning', 'Avalanche Watch', 'Beach Hazards Statement', 'Blizzard Warning', 'Blizzard Watch',
            'Blowing Dust Advisory', 'Blowing Dust Warning', 'Brisk Wind Advisory', 'Child Abduction Emergency',
            'Civil Danger Warning', 'Civil Emergency Message', 'Coastal Flood Advisory', 'Coastal Flood Statement',
            'Coastal Flood Warning', 'Coastal Flood Watch', 'Dense Fog Advisory', 'Dense Smoke Advisory',
            'Dust Advisory', 'Dust Storm Warning', 'Earthquake Warning', 'Evacuation - Immediate',
            'Excessive Heat Warning', 'Excessive Heat Watch', 'Extreme Cold Warning', 'Extreme Cold Watch',
            'Extreme Fire Danger', 'Extreme Wind Warning', 'Fire Warning', 'Fire Weather Watch',
            'Flash Flood Statement', 'Flash Flood Warning', 'Flash Flood Watch', 'Flood Advisory', 'Flood Statement',
            'Flood Warning', 'Flood Watch', 'Freeze Warning', 'Freeze Watch', 'Freezing Fog Advisory',
            'Freezing Rain Advisory', 'Freezing Spray Advisory', 'Frost Advisory', 'Gale Warning', 'Gale Watch',
            'Hard Freeze Warning', 'Hard Freeze Watch', 'Hazardous Materials Warning', 'Hazardous Seas Warning',
            'Hazardous Seas Watch', 'Hazardous Weather Outlook', 'Heat Advisory', 'Heavy Freezing Spray Warning',
            'Heavy Freezing Spray Watch', 'High Surf Advisory', 'High Surf Warning', 'High Wind Warning',
            'High Wind Watch', 'Hurricane Force Wind Warning', 'Hurricane Force Wind Watch',
            'Hurricane Local Statement', 'Hurricane Warning', 'Hurricane Watch', 'Hydrologic Advisory',
            'Hydrologic Outlook', 'Ice Storm Warning', 'Lake Effect Snow Advisory', 'Lake Effect Snow Warning',
            'Lake Effect Snow Watch', 'Lake Wind Advisory', 'Lakeshore Flood Advisory', 'Lakeshore Flood Statement',
            'Lakeshore Flood Warning', 'Lakeshore Flood Watch', 'Law Enforcement Warning', 'Local Area Emergency',
            'Low Water Advisory', 'Marine Weather Statement', 'Nuclear Power Plant Warning',
            'Radiological Hazard Warning', 'Red Flag Warning', 'Rip Current Statement', 'Severe Thunderstorm Warning',
            'Severe Thunderstorm Watch', 'Severe Weather Statement', 'Shelter In Place Warning', 'Short Term Forecast',
            'Small Craft Advisory', 'Small Craft Advisory For Hazardous Seas', 'Small Craft Advisory For Rough Bar',
            'Small Craft Advisory For Winds', 'Small Stream Flood Advisory', 'Snow Squall Warning',
            'Special Marine Warning', 'Special Weather Statement', 'Storm Surge Warning', 'Storm Surge Watch',
            'Storm Warning', 'Storm Watch', 'Test', 'Tornado Warning', 'Tornado Watch',
            'Tropical Depression Local Statement', 'Tropical Storm Local Statement', 'Tropical Storm Warning',
            'Tropical Storm Watch', 'Tsunami Advisory', 'Tsunami Warning', 'Tsunami Watch', 'Typhoon Local Statement',
            'Typhoon Warning', 'Typhoon Watch', 'Urban And Small Stream Flood Advisory', 'Volcano Warning',
            'Wind Advisory', 'Wind Chill Advisory', 'Wind Chill Warning', 'Wind Chill Watch', 'Winter Storm Warning',
            'Winter Storm Watch', 'Winter Weather Advisory']


def valid_areas():
    return ['AL', 'AK', 'AS', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL',
            'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
            'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
            'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY', 'PZ', 'PK', 'PH', 'PS', 'PM', 'AN', 'AM', 'GM', 'LS',
            'LM', 'LH', 'LC', 'LE', 'LO']


def eliminate_none_in_param_d(params):
    itr = copy.deepcopy(params)
    for key, value in itr.items():
        if value is None:
            params.pop(key)


def valid_zones():
    return []
