from warnings import warn
import copy
import pint

from nwsapy.core.inheritance.request_error import RequestError
from nwsapy.core.inheritance.base_endpoint import BaseEndpoint

class Point(BaseEndpoint):
    
    def __repr__(self):
        return f"Point object located at {self.lat}, {self.lon} ({self.city}, {self.state})"

    def __init__(self, lat, lon, user_agent):
        super().__init__()
        
        self._validate_input(lat = lat, lon = lon)
        self.lat = round(lat, 4)
        self.lon = round(lon, 4)
        
        url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        response = self._request_api(url, user_agent)
        
        if self.has_any_request_errors:
            self.values = RequestError(response)
        else:
            response = response.json()['properties']

            response['forecastZoneUrl'] = response['forecastZone']
            response['forecastZone'] = response['forecastZone'].split("/")[-1]

            response['countyUrl'] = response['county']
            response['county'] = response['county'].split("/")[-1]

            response['fireWeatherZoneUrl'] = response['fireWeatherZone']
            response['fireWeatherZone'] = response['fireWeatherZone'].split("/")[-1]

            rloc_props = response['relativeLocation']['properties']
            response['city'] = rloc_props['city']
            response['state'] = rloc_props['state']
            response['bearing'] = rloc_props['bearing']
            response['distance'] = rloc_props['distance']

            for k, v in response.items():
                setattr(self, k, v)
    
    # Validating the input from the user before requesting to the API.
    def _validate_input(self, **kwargs):
        # iterate through lat/lon values and validate them.
        for key, value in kwargs.items():
            valid_dtype = any([isinstance(value, int), isinstance(value, float)])
            if not valid_dtype:
                msg = f"{key} is not valid data type. Expected: int/float, Got: {type(value)}"
                raise ValueError(msg)
            
            if key == 'lat':
                if not -90 <= value <= 90:
                    msg = f'Latitude is not between -90 and 90. Got: {value}'
                    raise ValueError(msg)
            if key == 'lon':
                if not -180 <= value <= 180:
                    msg = f'Longitude not between -180 and 180. Got: {value}'
                    raise ValueError(msg)

    def to_dict(self) -> dict:        
        """Returns a dictionary with all of the attributes to the class.

        :return: Dictionary of the attributes of the class.
        :rtype: dictionary
        """
        return self.__dict__

    def to_pint(self, unit_registry : pint.UnitRegistry) -> object:
        """Returns a new self object with units using Pint. It does NOT update
        in-place.

        :param unit_registry: Your unit registry used in your application.
        :type unit_registry: pint.UnitRegistry
        :return: Dictionary with values converted to pint units.
        :rtype: dictionary
        """

        # Need to create a deep copy, behavior of dictionaries are different
        #   than lists, they don't create a copy of themselves
        new_point_obj = copy.deepcopy(self)
        
        # check each attribute, then create
        if hasattr(self, 'distance'):
            distance = self.distance['value'] * unit_registry.meter
            new_point_obj.distance = distance
            new_point_obj.series['distance'] = distance
        if hasattr(self, 'stations'):
            for station in self.stations:
                station_elevation = station.elevation['value'] * unit_registry.meter
                station.elevation = station_elevation
                station.series['elevation'] = station_elevation
        if hasattr(self, 'bearing'):
            bearing = self.bearing['value'] * unit_registry.degrees
            new_point_obj.bearing = bearing
            new_point_obj.series['bearing'] = bearing

        return new_point_obj