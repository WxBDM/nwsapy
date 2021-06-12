"""
This is the points module for wrapping the points portion in the API.

Specifically, this module holds classes for the following urls:
    ``/points/{point}``\n
    ``/points/{point}/stations``\n

You can find the API documentation here: https://www.weather.gov/documentation/services-web-api#/
"""
import copy

import pint
from shapely.geometry import Point as pt
import pandas as pd
import numpy as np

from nwsapy.errors import ParameterTypeError
import nwsapy.utils as utils


class PointsError(utils.ErrorObject):

    def __init__(self, response):
        """An Error object for the alerts endpoints.

        Attributes
        ----------
        type: str
            A URI reference (RFC3986) that identifies the problem type.

        title: str
            A short, human-readable summary of the problem type.

        status: int
            The HTTP status code (RFC7231, Section 6) generated by the origin server for this occurrence of the problem.
            Minimum: 100, Max 999

        detail: str
            A human-readable explanation specific to this occurrence of the problem.

        instance: string
            A URI reference that identifies the specific occurrence of the problem.

        correlationId: str
            A unique identifier for the request, used for NWS debugging purposes.
            Please include this identifier with any correspondence to help the API maintainers investigate your issue.
        """

        super().__init__(response)


class BasePoint(utils.ObjectIterator):

    n_errors = 0
    has_any_request_errors = True

    def _validate(self, lat, lon):
        valid_lat = (isinstance(lat, int), isinstance(lat, float))
        if not any(valid_lat):
            raise ParameterTypeError(lat, "int or float")

        valid_lon = (isinstance(lon, int), isinstance(lon, float))
        if not any(valid_lon):
            raise ParameterTypeError(lon, "int or float")

    def to_dict(self) -> dict:
        return self.__dict__

    def to_pint(self, unit_registry : pint.UnitRegistry) -> object:
        """Returns a new self object with units using Pint.

        Parameters
        ----------
        unit_registry: pint.UnitRegistry
            Your unit registry used in your application.
        """

        new_point_obj = copy.deepcopy(self)
        if hasattr(self, 'distance'):
            distance = new_point_obj.distance['value'] * unit_registry.meter
            new_point_obj.distance = distance
            new_point_obj.series['distance'] = distance
        if hasattr(self, 'stations'):
            for station in new_point_obj.stations:
                station_elevation = station.elevation['value'] * unit_registry.meter
                station.elevation = station_elevation
                station.series['elevation'] = station_elevation
        if hasattr(self, 'bearing'):
            bearing = new_point_obj.bearing['value'] * unit_registry.degrees
            new_point_obj.bearing = bearing
            new_point_obj.series['bearing'] = bearing

        return new_point_obj


class Point(BasePoint):

    def __repr__(self):
        return f"Point object located at {self.lat}, {self.lon} ({self.city}, {self.state})"

    def __init__(self, lat, lon, user_agent):

        self._validate(lat, lon)

        self.lat = round(lat, 4)  # api puts it into 4 decimals anyways
        self.lon = round(lon, 4)

        response = utils.request(f"https://api.weather.gov/points/{lat},{lon}", headers=user_agent)
        self.response_headers = response.headers

        if not response.ok:  # successful retrieval.
            self.points = PointsError(response)
            self.n_errors += 1
            self.has_any_request_errors = True
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

            response['series'] = pd.Series(data = response)

            for k, v in response.items():
                setattr(self, k, v)


class Station:

    def __init__(self, station_info_d):
        # Assumes that station_info_d is one individual station (0, 1, etc)
        attribute_d = {}
        geom = station_info_d['geometry']
        props = station_info_d['properties']

        # put in the lat/lon in shapely geom
        # have to put in shapely.geometry.Point otherwise it'll try and call point from above.
        point = pt([geom['coordinates'][0], geom['coordinates'][1]])
        attribute_d['point'] = point
        attribute_d.update(props)

        self.series = pd.Series(attribute_d)

        for k, v in attribute_d.items():
            setattr(self, k, v)

    def to_dict(self) -> dict:
        return self.__dict__


class PointStation(BasePoint):

    def __init__(self, lat, lon, user_agent):

        self._validate(lat, lon)

        response = utils.request(f"https://api.weather.gov/points/{lat},{lon}/stations", headers=user_agent)
        self.response_headers = response.headers

        if not response.ok:  # successful retrieval.
            self.points = PointsError(response)
            self.n_errors += 1
            self.has_any_request_errors = True
        else:
            response = response.json()
            self.stations = [Station(x) for x in response['features']]

        self._iterable = self.stations # make this object iterable.

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

        df = df.fillna(value=np.nan)  # in case there is missing data
        return df