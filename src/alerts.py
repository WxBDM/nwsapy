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
import pprint

from shapely.geometry import Point, Polygon, MultiPoint
from datetime import datetime
import requests

from errors import ParameterTypeError, DataValidationError
import utils


class _AlertConstructor:
    """Alert constructor should construct the individual alert object. Note that this is all dynamic."""

    def _construct_alert(self, alert_list):
        alert_dictionary = alert_list['properties']
        if not isinstance(alert_list['geometry'], type(None)):
            alert_dictionary.update({'geometry' : alert_list['geometry']})
            self._construct_geometry(alert_dictionary)  # even though the dict is being updated, it returns nothing.
        else: # there's no geometry tag, so make them none.
            no_geometry = dict({"points": None, 'polygon': None, "points_collection": None})  # set to none
            alert_dictionary.update(no_geometry)

        self._construct_times(alert_dictionary)
        constructed_alert = self._construct_methods(alert_dictionary)
        return constructed_alert()

    def _construct_methods(self, alert_dictionary):
        """Constructs the object and returns it."""

        # these methods are ones that are going to be bound to the object. This is documented
        def repr(self): return "\n".join([f"{attr} : {alert_dictionary[attr]}" for attr in alert_dictionary])
        def string(self): return f"{alert_dictionary['event']} object"
        def sent_before(self, other): return self.sent > other.sent
        def sent_after(self, other): return self.sent < other.sent
        def effective_before(self, other): return self.effective > other.effective
        def effective_after(self, other): return self.effective < other.effective
        def onset_before(self, other): return self.onset > other.onset
        def onset_after(self, other): return self.onset < other.onset
        def expires_before(self, other): return self.expires > other.expires
        def expires_after(self, other): return self.expires < other.expires

        # Create the object and bind the method to it.
        alert = type(alert_dictionary['event'].replace(" ", "").lower(), (), alert_dictionary)
        alert.__repr__ = MethodType(repr, alert)
        alert.__str__ = MethodType(string, alert)
        alert.sent_before = MethodType(sent_before, alert)
        alert.sent_after = MethodType(sent_after, alert)
        alert.effective_before = MethodType(effective_before, alert)
        alert.effective_after = MethodType(effective_after, alert)
        alert.onset_before = MethodType(onset_before, alert)
        alert.onset_after = MethodType(onset_after, alert)
        alert.expires_before = MethodType(expires_before, alert)
        alert.expires_after = MethodType(expires_after, alert)

        return alert # we're not instantiating the object here. It's in the main construct method.

    def _construct_geometry(self, alert_dictionary):

        """Construct alert.polygon, alert.points, and alert.multipoint"""
        # determine the geometry kind. If it's a point, make a list of shapely point objects, and create a multipoint
        # object.

        # If there is a geometry, then make points and points collection at a minimum.
        geometry_type = alert_dictionary['geometry']['type']
        points = [Point(x[0], x[1]) for x in alert_dictionary['geometry']['coordinates'][0]]
        polygon_d = dict({'points' : points, 'points_collection': MultiPoint(points)})

        # If the geometry type is a polygon, make a polygon object as well. Otherwise set to none.
        if geometry_type == 'Polygon':
            polygon_d['polygon'] = Polygon(points)
        else: # only if it's a point (just in case, this needs to be tested)
            polygon_d['polygon'] = None

        alert_dictionary.update(polygon_d)

    def _construct_times(self, alert_dictionary):
        # convert times to a date time object.
        all_times = ['sent', 'effective', 'onset', 'expires', 'ends']
        for time in all_times:
            if not isinstance(alert_dictionary[time], type(None)):
                alert_dictionary[time] = datetime.fromisoformat(alert_dictionary[time])

    @staticmethod
    def _validate_alert_type(alert_type: Union[str, list]):

        # checks to make sure that the data type is correct and is validated against the various alert types.

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

        """
        self._validate_alert_type(alert_type)  # validate data

        if isinstance(alert_type, str):
            alert_type = [alert_type]  # keep it consistent with the logic and just make it into a list.

        # Equivalent list comp logic:
        # filtered_alerts = []
        # for alert in self.alerts:
        #     for type_of_alert in alert_type:
        #         if type_of_alert == alert.event:
        #             filtered_alerts.append(alert)

        filtered_alerts = [alert for type_of_alert in alert_type for alert in self.alerts
                           if type_of_alert.title() == alert.event]

        return filtered_alerts

    def get_number_of(self, alert_type: Union[str, list]) -> Union[int, list]:
        r"""A method to give you the number of alerts of a specific type that are active.

        Parameters
        ----------
        alert_type : str, list
            The type of alert to be searched. Not case sensitive. Examples: "Tornado Warning", "flood watch". If it's
            a list, it will return a list of the number of warnings in the order it's provided. For example,
            ``get_number_of(['Tornado Warning', 'Freeze Warning'])`` will return the number of tornado warnings
            and the number of freeze warnings (e.g. ``[1, 10]``)

        Raises
        ------
        nwsapi.ParameterTypeError
            If the parameter isn't the correct data type (string).
        nwsapi.DataValidationError
            If the alert type isn't a valid National Weather Service alert.

        Returns
        -------
        int, list
            The number of alerts that are of the alert type. If a list, the number of alerts in order of the parameter.

        """
        self._validate_alert_type(alert_type) # validate data
        if isinstance(alert_type, str):
            alert_type = [alert_type]  # this is only to make it consistent with logic below.

        # it's valid, get it from the counter.
        count = [self.counter[alert.title()] if alert.title() in self.counter else 0 for alert in alert_type]
        if len(count) == 1:  # if there's only one alert type that was given.
            return count[0]

        return count  # otherwise, return the list.


@dataclass
class ActiveAlerts(_AlertConstructor):
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
        response = utils.request("https://api.weather.gov/alerts/active")
        info = response.json()['features']
        self.alerts = [self._construct_alert(x) for x in info]  # opted for list comp because it's faster
        self.counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts


@dataclass
class AlertById(_AlertConstructor):
    r"""A class used to hold information about all active alerts found from ``alerts/active/{id}``

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    counter : collections.Counter
        A collection of the number of alerts there are based upon the event type.

    """

    def __init__(self, alert_id):

        self._validate(alert_id)
        if isinstance(alert_id, str):
            alert_id = [alert_id]  # this is only to make it consistent with logic below.

        self.alerts = []
        for a_id in alert_id: # iterate through the alerts
            response = utils.request(f"https://api.weather.gov/alerts/{a_id}")
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response) # if something weird went wrong, put an error repsonse in.
                # TODO: handle error responses.
                continue

            info = response.json() # all is good, construct the alert objects.
            self.alerts.append(self._construct_alert(info))

        self.counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

        # if there's only one value in the list, just make it the attribute.
        if len(self.alerts) == 1:
            self.alerts = self.alerts[0]

    def _validate(self, alert_id):

        # Validate the input data and provide ParameterTypeError.

        invalid = (isinstance(alert_id, str), isinstance(alert_id, list), isinstance(alert_id, tuple))
        if not any(invalid):  # if it's not string, list, or tuple
            raise ParameterTypeError(alert_id, 'string, list, or tuple')

        if isinstance(alert_id, str):
            alert_id = [alert_id]

        for alert in alert_id:
            if not isinstance(alert, str):
                raise ParameterTypeError(alert, "string")


@dataclass
class AlertByMarineRegion(_AlertConstructor):
    r"""A class used to hold information about all active alerts found from ``alerts/active/region/{region}``

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    counter : collections.Counter
        A collection of the number of alerts there are based upon the event type.

    See Also
    --------
    :ref:`Valid Data Points - Alerts by Marine Region<alerts_by_marine_table_validation>`
        Table in the documentation to show what regions are valid for this function.

    """

    # AL => Alaska
    # AT => Atlantic Marine
    # GL => Great Lakes
    # GM => Gulf of Mexico
    # PA => Pacific Marine
    # PI => Pacific Islands

    def __init__(self, region):

        self._validate(region) # make sure the data is valid.

        if isinstance(region, str):
            region = [region]  # make it a list, eliminates unnecessary if/else statements.

        self.alerts = []
        for region_str in region:
            region_str = region_str.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/region/{region_str}")
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(self._construct_alert(x))

        self.counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

        # if there's only one value in the list, just make it the attribute.
        if len(self.alerts) == 1:
            self.alerts = self.alerts[0]

    def _validate(self, data):
        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")

        # checking to make sure that the data is in the possible values.
        # For better details for the user, print a string of all of the bad data points.
        valid_list = ['AL', 'AT', 'GL', 'GM', 'PA', 'PI']
        invalid_data = [value for value in data if value.upper() not in valid_list]

        if len(invalid_data) > 0:
            raise DataValidationError(", ".join(invalid_data))


@dataclass
class AlertByArea(_AlertConstructor):
    r"""A class used to hold information about all active alerts found from ``alerts/active/area/{area}``

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    counter : collections.Counter
        A collection of the number of alerts there are based upon the event type.

    See Also
    --------
    :ref:`Valid Data Points - Alerts by Area Table<alerts_by_area_table_validation>`
        Table in the documentation to show what areas are valid for this function.

    """

    def __init__(self, area):
        self._validate(area)  # make sure the data is valid.

        if isinstance(area, str):
            area = [area]  # make it a list, eliminates unnecessary if/else statements.

        self.alerts = []
        for area_str in area:
            area_str = area_str.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/area/{area_str}")
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(self._construct_alert(x))

        self.counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

    def _validate(self, data):

        if isinstance(data, str):
            data = [data]

        valid_data = ['AL', 'AK', 'AS', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL',
                      'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                      'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
                      'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY', 'PZ', 'PK', 'PH', 'PS', 'PM', 'AN', 'AM', 'GM', 'LS',
                      'LM', 'LH', 'LC', 'LE', 'LO']

        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")

            if data_val.upper() not in valid_data:
                raise DataValidationError(data)


@dataclass
class AlertByCount:
    r"""A class used to hold information about all active alerts found from ``alerts/active/count``

    Attributes
    ----------
    total : int
        The total number of alerts
    land : int
        The total number of alerts over land
    marine : int
        The total number of alerts over water
    regions : dict
        Specifies the number of marine alerts in a certain location (keys: regions, values: int)
    areas : dict
        Specifies the number of land alerts in a certain location (keys: areas, values: int)
    zones : dict
        Specifies the number of alerts per zone (keys: zone, values: int)

    """

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

    def _filter_by(self, region_area_or_zone, filter, docs_str): # private method, used to refactor filter_x methods.
        """Used to refactor filter_x methods. Much cleaner this way."""

        valid = (isinstance(filter, str), isinstance(filter, list), isinstance(filter, tuple))
        if not valid:
            raise ParameterTypeError(filter, "string, list tuple")

        if isinstance(filter, str):
            filter = [filter]  # make it a list to be consistent with logic (eliminates unnecessary if/else)

        filtered_d = {}
        for filter_item in filter: # iterate through user inputs
            filter_item = filter_item.upper()
            if filter_item not in region_area_or_zone.keys(): # ensure that it's in the keys (see __init__)
                raise DataValidationError(filter_item, docs_str)
            filtered_d[filter_item] = region_area_or_zone[filter_item]

        return filtered_d

    def filter_marine_regions(self, region: Union[str, list, tuple]) -> list:
        r"""Filters all active alerts based upon the marine region.

        Parameters
        ----------
        region : str, list, or tuple
            The marine region that you want to filter by. See documentation for valid inputs.

        Returns
        -------
        dict
            Dictionary with key:value pairs being region:count.

        """
        return self._filter_by(self.regions, region, "Documentation link goes here.")


    def filter_land_areas(self, area: Union[str, list, tuple]) -> list:
        r"""Filters all active alerts based upon the land area.

        Parameters
        ----------
        area : str, list, or tuple
            The land area that you want to filter by. See documentation for valid inputs.

        Returns
        -------
        dict
            Dictionary with key:value pairs being area:count.

        """
        return self._filter_by(self.areas, area, "Documentation link goes here.")

    def filter_zones(self, zone: Union[str, list, tuple]) -> list:
        r"""Filters all active alerts based upon the marine region.

        Parameters
        ----------
        zone : str, list, or tuple
            The zone ID that you want to filter by. See documentation for valid inputs.

        Returns
        -------
        dict
            Dictionary with key:value pairs being zone:count.

        """
        return self._filter_by(self.zones, zone, "Documentation link goes here.")