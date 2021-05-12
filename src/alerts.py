"""
This is the alerts module for wrapping the alerts portion in the API.

Specifically, this module holds classes for the following urls:
    `/alerts`
    `/alerts/active`
    `/alerts/types`
    `/alerts/{id}`
    `/alerts/active/count`
    `/alerts/active/zone/{zoneId}`
    `/alerts/active/area/{area}`
    `/alerts/active/region/{region}`

You can find the API documentation here: https://www.weather.gov/documentation/services-web-api#/
"""
from dataclasses import dataclass
import collections

from shapely.geometry import Point, Polygon, MultiPoint
import requests

from errors import ParameterTypeError, DataValidationError
import utils


@dataclass
class Alert:
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
        alert = type(full_d['event'].replace(" ", "").lower(), (), full_d)
        return alert()  # this instantiates the object. Don't change this!

    @staticmethod
    def _validate_alert_type(alert_type: str):

        # checks to make sure that the data type is correct and is validated against the various alert types.

        # data checking.
        if not isinstance(alert_type, str):
            raise ParameterTypeError(alert_type, str)

        # make sure it's a valid product. If so, then we're okay to check inside of the collections.
        alert_type = alert_type.title()
        valid_product_link = "https://api.weather.gov/alerts/types"
        response = utils.request(valid_product_link)
        event_types = response.json()['eventTypes']
        if alert_type not in event_types:
            raise DataValidationError(alert_type)


@dataclass
class ActiveAlerts(Alert):
    r"""A class used to hold information about all active alerts.

    Each alert is it's own object type that is stored in a list (self.alerts). That is:
        > a tornado warning alert would be a tornadowarning object.
        > A small craft advisory alert would be a smallcraftadvisory object.

    Note
    ----
    There is minimal handling of requests. Error handling can be found in the utilities folder

    See Also
    --------
    utils.request() : handling of request errors

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    counter : collections.Counter
        A collection of the number of alerts there are based upon the event type.

    Methods
    -------
    get_number_of(alert_type: str) -> int
        Returns the number of alerts of this alert type.
    filter_by(alert_type: str) -> list
        Filters all of the alerts based off of the given alert type.

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

    def filter_by(self, alert_type: str) -> list:
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

        Examples
        --------
        >>> active_alerts = nwsapi.get_active_alerts()
        >>> all_flood_warnings = active_alerts.filter_by('Flood Warning')
        [<alerts.floodwarning object at 0x7fcf55199d00>, <alerts.floodwarning object at 0x7fcf5519cfd0>, ...]
        """
        self._validate_alert_type(alert_type)  # validate data

        filtered_alerts = [alert for alert in self.alerts if alert.event == alert_type]
        return filtered_alerts


@dataclass
class AlertById(Alert):

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

        # validate the data
        self._validate_alert_type(alert_type)

        # filter the alerts
        filtered_alerts = [alert for alert in self.alerts if alert.event == alert_type]
        return filtered_alerts


@dataclass
class AlertByCount(Alert):

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
