"""
This is the alerts module for wrapping the alerts portion in the API.

Specifically, this module holds classes for the following urls:
    ``/alerts``\n
    ``/alerts/active``\n
    ``/alerts/types``\n
    ``/alerts/{id}``\n
    ``/alerts/active/count``\n
    ``/alerts/active/zone/{zoneId}``\n
    ``/alerts/active/area/{area}``\n
    ``/alerts/active/region/{region}``\n

You can find the API documentation here: https://www.weather.gov/documentation/services-web-api#/
"""
from dataclasses import dataclass
from types import MethodType
from typing import Union
import collections

from shapely.geometry import Point, Polygon, MultiPoint
import requests

from errors import ParameterTypeError, DataValidationError
import utils


@dataclass
class _Alert:
    # Base class for alerts sub classes.

    @staticmethod
    def _sort_geometry(alert_list):
        # determine the geometry kind. If it's a point, make a list of shapely point objects, and create a multipoint
        # object.
        if isinstance(alert_list['geometry'], type(None)):  # if there's no geometry (i.e. 'geometry' : null)
            polygon_d = dict(points=None, polygon=None, points_collection=None)  # set to none. This is to remain to consistent
        else:
            # If there is a geometry, then make points and points collection at a minimum.
            geometry_type = alert_list['geometry']['type']
            points = [Point(x[0], x[1]) for x in alert_list['geometry']['coordinates'][0]]
            points_collection = MultiPoint(points)
            polygon_d = dict({'points': points, 'points_collection': points_collection})

            # If the geometry type is a polygon, make a polygon object as well. Otherwise set to none.
            if geometry_type == 'Polygon':
                polygon_d['polygon'] = Polygon(points)
            else:
                polygon_d['polygon'] = None

        # properties is a nested dictionary. Need to create a new dictionary and then update it with logic from above.
        full_d = alert_list['properties']
        full_d.update(polygon_d)

        # this will be the object that's created based on the event.
        #    for example, if it was a tornado warning, the object would be "tornadowarning"

        def str_obj_info(self):
            info = [f"{attribute} : {full_d[attribute]}" for attribute in full_d]
            return "\n".join(info)

        alert = type(full_d['event'].replace(" ", "").lower(), (), full_d)
        alert.peek_at_info = MethodType(str_obj_info, alert)
        return alert()  # this instantiates the object. Don't change this!

    @staticmethod
    def _validate_alert_type(alert_type: Union[str, list]):

        # checks to make sure that the data type is correct and is validated against the various alert types.

        # data checking.
        invalid = (isinstance(alert_type, str), isinstance(alert_type, list), isinstance(alert_type, tuple))
        if not any(invalid): # if it's not string, list, or tuple
            raise ParameterTypeError(alert_type, 'string, list, or tuple')

        if isinstance(alert_type, str):
            alert_type = [alert_type]

        # make sure it's a valid product. If so, then we're okay to check inside of the collections.
        valid_product_link = "https://api.weather.gov/alerts/types"
        response = utils.request(valid_product_link)
        event_types = response.json()['eventTypes']
        for alert in alert_type:
            alert = alert.title()
            if alert not in event_types:
                raise DataValidationError(alert)


@dataclass
class ActiveAlerts(_Alert):
    r"""A class used to hold information about all active alerts found from ``alerts/active``

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    counter : collections.Counter
        A collection of the number of alerts there are based upon the event type.

    """

    def __init__(self):
        """Instantiate the ActiveAlerts object.

        This sends a request to /alerts/active, then stores all of the alerts based off of it's type in a list.
        There is also an attribute to count the number of alerts (collections.Counter).

        Note
        ----
        As of release, there is no way to handle bad requests from the server. It will likely result in a KeyError.
        """
        response = utils.request("https://api.weather.gov/alerts/active")
        info = response.json()['features']
        self.alerts = [self._sort_geometry(x) for x in info]  # opted for list comp because it's faster
        self.counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

    def get_number_of(self, alert_type: str) -> int:
        r"""A method to give you the number of alerts of a specific type that are active.

        Parameters
        ----------
        alert_type : str
            The type of alert to be searched. Not case sensitive. Examples: "Tornado Warning", "flood watch"

        Raises
        ------
        nwsapi.ParameterTypeError
            If the parameter isn't the correct data type (string).
        nwsapi.DataValidationError
            If the alert type isn't a valid National Weather Service alert.

        Returns
        -------
        int
            The number of alerts that are of the alert type.

        Examples
        --------
        >>> active_alerts = nwsapi.get_alert_count()
        >>> active_alerts.get_alert_count('Flood Warning')
        35
        """
        self._validate_alert_type(alert_type) # validate data

        # valid data type, valid product. Get it from counter. (O(1))
        if alert_type not in self.counter:
            return 0
        else:
            return self.counter[alert_type]

    def filter_by(self, alert_type: Union[str, list]) -> list:
        r"""Filters all active alerts based upon the alert type.

        Parameters
        ----------
        alert_type : str, list
            The type of alert to be searched. Not case sensitive.
            Examples: "Tornado Warning", ["flood watch", "SmAlL CrAfT wArNiNg"]

        Raises
        ------
        nwsapi.ParameterTypeError
            If the parameter isn't the correct data type (string).
        nwsapi.DataValidationError
            If the alert type isn't a valid National Weather Service alert.

        Returns
        -------
        list
            A collection of the filtered alert objects based upon the parameter.

        Examples
        --------
        Suppose you wanted to get all flood warnings:

        >>> active_alerts = nwsapy.get_active_alerts()
        >>> all_flood_warnings = active_alerts.filter_by('Flood Warning')
        [<alerts.floodwarning object at 0x7fcf55199d00>,
        <alerts.floodwarning object at 0x7fcf5519cfd0>, ...]

        Suppose you wanted to get all air quality alerts and special weather statements:

        >>> active_alerts = nwsapy.get_active_alerts()
        >>> all_flood_warnings = active_alerts.filter_by(["Air QUALITY alert", "Special Weather stAteMenT"])
        [<alerts.airqualityalert object at 0x7fc1c9169640>, ...,
        <alerts.specialweatherstatement object at 0x7fc1c916d610>, ...]

        """
        self._validate_alert_type(alert_type)  # validate data

        if isinstance(alert_type, str):
            alert_type = [alert_type] # keep it consistent with the logic and just make it into a list.

        # Equivalent list comp logic:
        # filtered_alerts = []
        # for alert in self.alerts:
        #     for type_of_alert in alert_type:
        #         if type_of_alert == alert.event:
        #             filtered_alerts.append(alert)

        filtered_alerts = [alert for type_of_alert in alert_type for alert in self.alerts
                           if type_of_alert.title() == alert.event]

        return filtered_alerts


@dataclass
class AlertById(_Alert):

    def __init__(self, alert_id):

        self.alerts = []

        self._validate_parameter(alert_id)
        if isinstance(alert_id, str):
            alert_id = [alert_id]  # this is only to make it consistent and easier to read code.

        for a_id in alert_id:
            response = utils.request(f"https://api.weather.gov/alerts/{a_id}")
            if not isinstance(response, requests.Response):
                self.alerts.append(response)
                continue

            info = response.json()
            del info['@context']
            self.alerts.append(self._sort_geometry(info))

        self.counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

        # if there's only one value in the list, just make it the attribute.
        if len(self.alerts) == 1:
            self.alerts = self.alerts[0]

    def _validate_parameter(self, alert_id):

        # test to see if it's either str, list, or tuple.
        validation = (isinstance(alert_id, str), isinstance(alert_id, list), isinstance(alert_id, tuple))
        if not any(validation):
            raise ValueError(f"alert_id should be a string. Got: {type(alert_id)}")

    def filter_by(self, alert_type):
        r"""Filters all active alerts based upon the alert type.

        Parameters
        ----------
        alert_type : str
            The type of alert to be searched. Not case sensitive. Examples: "Tornado Warning", "flood watch"

        Raises
        ------
        nwsapi.ParameterTypeError
            If the parameter isn't the correct data type (string).
        nwsapi.DataValidationError
            If the alert type isn't a valid National Weather Service alert.

        Returns
        -------
        list
            A collection of the filtered alert objects based upon the parameter.

        Example
        -------
        >>> active_alerts = nwsapy.get_active_alerts()
        >>> all_flood_warnings = active_alerts.filter_by('Flood Warning')
        [<alerts.floodwarning object at 0x7fcf55199d00>,
            <alerts.floodwarning object at 0x7fcf5519cfd0>, ...]
        """
        # validate the data
        self._validate_alert_type(alert_type)

        # filter the alerts
        filtered_alerts = [alert for alert in self.alerts if alert.event == alert_type]
        return filtered_alerts


@dataclass
class AlertByMarineRegion(_Alert):

    """Not yet implemented."""
    pass


@dataclass
class AlertByArea(_Alert):

    """Not yet implemented."""
    pass


@dataclass
class AlertByCount(_Alert):

    """Not yet implemented."""

    def __init__(self):
        url = "https://api.weather.gov/alerts/active/count"
        response = utils.request(url)
        info = response.json()

        self.total = info['total']  # dtype: int
        self.land = info['land']  # dtype: int
        self.marine = info['marine']  # dtype: int
        self.regions = info['regions']  # dtype: dict {str : int}
        self.areas = info['areas']  # dtype: dict {str : int}
        self.zones = info['zones']  # dtype: dict {str : int}
