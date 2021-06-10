"""
This is the points module for wrapping the points portion in the API.

Specifically, this module holds classes for the following urls:
    ``/points/{point}``\n
    ``/points/{point}/stations``\n

You can find the API documentation here: https://www.weather.gov/documentation/services-web-api#/
"""
from typing import Union, Optional
import collections
import copy

from shapely.geometry import Point
import pandas as pd
import numpy as np
import requests
import shapely

from nwsapy.errors import ParameterTypeError
import nwsapy.utils as utils


class BasePoint:

    def to_pint(self, unit_registry) -> object:
        """Returns a new self object with units using Pint.

        Parameters
        ----------
        unit_registry
            Your unit registry used in your application.

        """
        ureg = unit_registry

        new_point_obj = copy.deepcopy(self)
        if hasattr(self, 'distance'):
            new_point_obj.distance = new_point_obj.distance['value'] * ureg.meter
        if hasattr(self, 'stations'):
            for station in new_point_obj.stations:
                station.elevation = station.elevation['value'] * ureg.meter

        return new_point_obj


class Point(BasePoint):

    def __init__(self, lat, lon, user_agent):

        self._validate(lat, lon)

        self.lat = round(lat, 4)  # api puts it into 4 decimals anyways
        self.lon = round(lon, 4)

        response = utils.request(f"https://api.weather.gov/points/{lat},{lon}", headers=user_agent)
        self.response_headers = response.headers
        if not isinstance(response, requests.models.Response):  # successful retrieval.
            self.response = [response]
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

    def __repr__(self):
        return f"Point object located at {self.lat}, {self.lon} ({self.city}, {self.state})"

    def _validate(self, lat, lon):
        valid_lat = (isinstance(lat, int), isinstance(lat, float))
        if not any(valid_lat):
            raise ParameterTypeError(lat, "int or float")

        valid_lon = (isinstance(lon, int), isinstance(lon, float))
        if not any(valid_lon):
            raise ParameterTypeError(lon, "int or float")


class Station:

    def __init__(self, station_info_d):
        # Assumes that station_info_d is one individual station (0, 1, etc)
        attribute_d = {}
        geom = station_info_d['geometry']
        props = station_info_d['properties']

        # put in the lat/lon in shapely geom
        # have to put in shapely.geometry.Point otherwise it'll try and call point from above.
        point = shapely.geometry.Point([geom['coordinates'][0], geom['coordinates'][1]])
        attribute_d['point'] = point
        attribute_d.update(props)

        self.series = pd.Series(attribute_d)

        for k, v in attribute_d.items():
            setattr(self, k, v)


class PointStation(BasePoint):

    def __init__(self, lat, lon, user_agent):
        response = utils.request(f"https://api.weather.gov/points/{lat},{lon}/stations", headers=user_agent)
        self.response_headers = response.headers
        if isinstance(response, requests.models.Response):  # successful retrieval.
            response = response.json()
            self.error = None
        else:
            self.error = [response]

        self.stations = [Station(x) for x in response['features']]

    def to_dataframe(self) -> pd.DataFrame:
        r"""Converts all of all retrieved alerts into a Pandas dataframe.

        Returns
        -------
        pandas.DataFrame
            A dataframe that contains the information (attributes) of all of the point requested.
        """
        df = pd.DataFrame()
        for station in self.stations:
            df = df.append(station.series, ignore_index=True) # append the series.

        df = df.fillna(value=np.nan) # in case there is missing data
        return df
