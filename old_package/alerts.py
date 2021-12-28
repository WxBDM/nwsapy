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

You can find the API documentation here: 
https://www.weather.gov/documentation/services-web-api#/
"""
import copy
import warnings

import shapely
from shapely.geometry import Point
from datetime import datetime
import pandas as pd
import pytz
import numpy as np
import requests

from old_package.errors import ParameterTypeError, DataValidationError
from old_package.url_constructor import AlertURLConstructor
import old_package.utils as utils


class AlertError(utils.ErrorObject):
    """An Error object for the alerts endpoints.

    Attributes
    ----------
    type: str
        A URI reference (RFC3986) that identifies the problem type.
    title: str
        A short, human-readable summary of the problem type.
    status: int
        The HTTP status code (RFC7231, Section 6) generated by the origin server 
        for this occurrence of the problem.
        Minimum: 100, Max 999
    detail: str
        A human-readable explanation specific to this occurrence of the problem.
    instance: string
        A URI reference that identifies the specific occurrence of the problem.
    correlationId: str
        A unique identifier for the request, used for NWS debugging purposes.
        Please include this identifier with any correspondence to help the API 
        maintainers investigate your issue.
    """
    def __init__(self, response):
        super().__init__(response)


class IndividualAlert:
    """Individual alert class, holds properties describing each individual 
    alert.

    Attributes
    ----------
    affectedZones: list[str]
        A list of affected zones by ID.

    areaDesc: str
        A description of the area that the alert covers.

    category: str
        The category in which the alert falls under.

    description: str
        Describes the alert.

    effective: datetime.datetime
        When the alert is effective (local time)

    effective_utc: datetime.datetime
        When the alert is effective (local time)

    ends: datetime.datetime or None
        When the alert ends (local time)

    ends_utc: datetime.datetime or None
        When the alert ends (UTC time)

    event: str
        The event of which this alert is (used as the object type)

    expires: datetime.datetime or None
        When the alert ends (local time)

    expires_utc: datetime.datetime or None
        When the alert ends (UTC time)

    geocode: dict

    headline: str
        The headline of the alert.

    id: str
        The associated ID of the alert.

    instruction: str
        The “call to action” of the alerrt.

    messageType: str
        What kind of message the alert is (update, warning, etc)

    onset: datetime.datetime
        When the alert was onset (local time).

    onset_utc: datetime.datetime
        When the alert was onset (UTC time).

    parameters: dict

    points: list, containing shapely.Point or None
        Points where the alert lies (lat/lon)

    polygon: shapely.Polygon or None
        The polygon where the alert lies.

    references: list

    sender: str
        Who sent the alert.

    senderName: str
        Which NWS office sent the alert.

    sent: datetime.datetime
        When the alert was sent (local time)

    sent_utc: datetime.datetime
        When the alert was sent (UTC time)

    series: pandas.Series
        A pandas series with all attributes of this object

    severity: str
        The severity level of the alert.

    status: str
        The status level of the alert.

    urgency: str
        The urgency level of the alert.
    """

    def __init__(self, alert_list):
        alert_d = alert_list['properties'] # prep to set all attributes

        # set all attributes
        geom_d = self._format_geometry(alert_list['geometry'])
        alert_d.update(geom_d)

        # set all times
        times = {'sent': alert_d['sent'], 'effective': alert_d['effective'],
                 'onset': alert_d['onset'], 'expires': alert_d['expires'], 
                 'ends': alert_d['ends']}
        time_d = self._set_times(times)
        alert_d.update(time_d)

        # fix the affected zones so it's only the zoneID.
        alert_d['affectedZones'] = [zone.split("/")[-1] for zone in alert_d['affectedZones']]
        alert_d['areaDesc'] = alert_d['areaDesc'].split(";")

        for k, v in alert_d.items():
            setattr(self, k, v)

        self.series = pd.Series(alert_d)
        self._d = alert_d  # used for to_dict(). __dict__ doesn't get class variables.

    def _format_geometry(self, geometries):
        if not isinstance(geometries, type(None)):  # if there's any kind of geometry
            geometry_type = geometries['type']

            # First check to see if it's a multipolygon. If so, then we need to create polygons out of it.
            if geometry_type == "MultiPolygon":
                points = []
                polygons = []
                for polygon in geometries['coordinates']:
                    polygon_points = [Point(x[0], x[0]) for x in polygon[0]]
                    points.append(polygon_points)
                    polygons.append(shapely.geometry.Polygon(polygon_points))

                return dict({"points" : points, "polygon" : polygons})

            # determine the geometry kind. If it's a point, make a list of shapely point objects.
            points = [Point(x[0], x[1]) for x in geometries['coordinates'][0]]
            polygon_d = dict({'points': points})

            # If the geometry type is a polygon, make a polygon object as well. Otherwise set to none.
            if geometry_type == 'Polygon':
                polygon_d['polygon'] = shapely.geometry.Polygon(points)
            else:  # only if it's a point (just in case, this needs to be tested)
                polygon_d['polygon'] = None

        else:  # there's no geometry tag, so make them none.
            polygon_d = dict({"points": None, 'polygon': None})  # set to none

        return polygon_d

    def _set_times(self, times):
        utc = pytz.timezone("UTC")
        time_d = {}
        for time in times:
            if not isinstance(times[time], type(None)):
                time_d[time] = datetime.fromisoformat(times[time])
                time_d[time + "_utc"] = time_d[time].astimezone(utc)
            else:
                time_d[time] = None
                time_d[time + "_utc"] = None

        return time_d

    def to_dict(self):
        r"""Converts all of the attributes to a dictionary.

        Returns
        -------
        dict
            A dictionary containing all of the attributes of the object.
        """
        return self._d

    def sent_before(self, other):
        """Method to compare sent times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.sent_utc > other.sent_utc

    def sent_after(self, other):
        """Method to compare sent times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was after before other. False otherwise."""
        return self.sent_utc < other.sent_utc

    def effective_before(self, other):
        """Method to compare effective times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.effective_utc > other.effective_utc

    def effective_after(self, other):
        """Method to compare effective times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was after before other. False otherwise."""
        return self.effective_utc < other.effective_utc

    def onset_before(self, other):
        """Method to compare onset times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.onset_utc > other.onset_utc

    def onset_after(self, other):
        """Method to compare onset times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent after other. False otherwise."""
        return self.onset_utc < other.onset_utc

    def expires_before(self, other):
        """Method to compare expire times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.expires_utc > other.expires_utc

    def expires_after(self, other):
        """Method to compare expire times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent after other. False otherwise."""
        return self.expires_utc < other.expires_utc

    def ends_before(self, other):
        """Method to compare end times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.ends_utc > other.ends_utc

    def ends_after(self, other):
        """Method to compare end times. All times are compared in UTC.

        Parameters
        ----------
        other: alerts.IndividualAlert
            Another individual alert object.

        Returns
        -------
        bool
            True if this alert was sent after other. False otherwise."""
        return self.ends_utc < other.ends_utc


class BaseAlert(utils.ObjectIterator):

    n_errors = 0  # count the number of errors in the alert object.
    has_any_request_errors = False
    url_constructor = AlertURLConstructor()

    def _init_active_and_all(self, response):
        """Set the attributes for active and all alerts."""

        if not response.ok:
            self.alerts = AlertError(response)
            self.n_errors += 1
            self.has_any_request_errors = True
        else:
            info = response.json()['features']
            self.alerts = [IndividualAlert(x) for x in info if x['properties']['event'] != 'Test Message']

        self._iterable = self.alerts # make the object iterable.
        self.response_headers = response.headers

    def _init_area_zone_marine(self, which: str, endpoint_list: list, user_agent):

        if which == 'area':
            url = 'https://api.weather.gov/alerts/active/area/'
        elif which == 'zone':
            url = "https://api.weather.gov/alerts/active/zone/"
        elif which == 'marine':
            url = 'https://api.weather.gov/alerts/active/region/'

        self.alerts = []
        self.response_headers = []
        for endpoint_str in endpoint_list:
            response = utils.request(f"{url}{endpoint_str.upper()}", headers=user_agent)
            if not response.ok:  # if it's a bad response (404, 500, etc)
                self.alerts.append(AlertError(response))
                self.response_headers.append(response.headers)
                self.n_errors += 1
                self.has_any_request_errors = True
            else:
                info = response.json()['features']
                for x in info:
                    if x['properties']['event'] != 'Test Message':
                        self.alerts.append(IndividualAlert(x))

            self.response_headers.append(response.headers)

        self._iterable = self.alerts  # make the object iterable.

    def to_dataframe(self) -> pd.DataFrame:
        r"""Converts all of all retrieved alerts into a Pandas dataframe.

        Returns
        -------
        pandas.DataFrame
            A dataframe that contains the information (attributes) of all of the alerts requested.
        """
        df = pd.DataFrame()
        for alert in self.alerts:
            df = df.append(alert.series, ignore_index=True)  # append the series.

        df = df.fillna(value=np.nan)  # in case there is missing data
        return df

    def to_dict(self) -> dict:
        r"""Converts all of the attributes to a dictionary.

        Returns
        -------
        dict
            A dictionary containing all of the attributes of the object.
        """

        return self.__dict__


class AllAlerts(BaseAlert):
    r"""A class used to hold information about all alerts found from ``/alerts``.

    Attributes
    ----------
    alerts : list[alerts.IndividualAlert or alerts.Error]
        A list containing alerts.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.
    """

    def __init__(self, user_agent, param_d):
        if len(param_d) != 0:
            url = self.url_constructor.all_alert_url_constructor(param_d)
        else:
            url = "https://api.weather.gov/alerts"
        self.response = utils.request(url, headers=user_agent)
        self._init_active_and_all(self.response)


class ActiveAlerts(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active``.

    Attributes
    ----------
    alerts : list[alerts.IndividualAlert or alerts.Error]
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.
    """

    def __init__(self, user_agent, param_d):
        if len(param_d) != 0:
            url = self.url_constructor.active_alert_url_constructor(param_d)
        else:
            url = "https://api.weather.gov/alerts/active"
        self.response = utils.request(url, user_agent)
        self._init_active_and_all(self.response)


class AlertById(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/{id}``.

    Attributes
    ----------
    alerts : list[alerts.IndividualAlert or alerts.Error]
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.
    """

    def __init__(self, alert_id, user_agent):

        # This is not refactored to the base alert class because the logic in the init function is
        #   slightly different. There isn't ['features']. There's also no point in filtering out the test
        #   message, as they're getting a specific alert by ID. If the user gets it, it's their fault.

        alert_id = self._validate(alert_id)

        self.alerts = []
        self.response_headers = []  # it's 1 alert at a time, so keep it ordered.
        for a_id in alert_id:  # iterate through the alerts
            response = utils.request(f"https://api.weather.gov/alerts/{a_id}", user_agent)
            if not response.ok:
                self.alerts.append(AlertError)
                self.response_headers.append(response.headers)
                self.n_errors += 1
                self.has_any_request_errors = True
                continue

            # no need to do response.json()['features'], as it's only one alert at a time.
            info = response.json()  # all is good, construct the alert objects

            # not going to filter out test message. If they get it, their fault.
            self.alerts.append(IndividualAlert(info))
            self.response_headers.append(response.headers)

        self._iterable = self.alerts # make the object iterable.

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

        return alert_id


class AlertByMarineRegion(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/region/{region}``.

    Attributes
    ----------
    alerts : list[alerts.IndividualAlert or alerts.Error]
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    See Also
    --------
    :ref:`Valid Data Points - Alerts by Marine Region<alerts_by_marine_table_validation>`
        Table in the documentation to show what regions are valid for this function.
    """

    def __init__(self, region, user_agent):

        region = self._validate(region)  # make sure the data is valid.
        self._init_area_zone_marine('marine', region, user_agent)

    def _validate(self, data):

        valid_data = ["AL", "AT", "GL", "GM", "PA", "PI"]

        if isinstance(data, str):
            data = [data]

        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")

            if data_val.upper() not in valid_data:
                raise DataValidationError(data_val)

        return data


class AlertByArea(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/area/{area}``.

    Attributes
    ----------
    alerts : list[alerts.IndividualAlert or alerts.Error]
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    See Also
    --------
    :ref:`Valid Data Points - Alerts by Area Table<alerts_by_area_table_validation>`
        Table in the documentation to show what areas are valid for this function.
    """

    def __init__(self, area, user_agent):
        area = self._validate(area)  # make sure the data is valid.
        self._init_area_zone_marine('area', area, user_agent)

    def _validate(self, data):

        valid_data = utils.valid_areas()

        if isinstance(data, str):
            data = [data]

        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")

            if data_val.upper() not in valid_data:
                raise DataValidationError(data)

        return data


class AlertByZone(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/zone/{zoneId}``.

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list[alerts.IndividualAlert or alerts.Error]
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    Note
    ----
    This does not have data validation checks, so ensure that your zone ID's are correct, otherwise
    you may run into a 404 error.
    """

    def __init__(self, zoneID, user_agent):

        zoneID = self._validate(zoneID)  # make sure the data is valid.
        self._init_area_zone_marine('zone', zoneID, user_agent)

    def _validate(self, data):

        if isinstance(data, str):
            data = [data]

        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")

        return data


class AlertByCount:
    r"""A class used to hold information about all active alerts found from ``alerts/active/count``

    Note: If successful, all attributes except ``alerts`` will be set to ``None``. If unsuccessful, all attributes
    except ``alerts`` will be set to ``None``. Keep in mind that ``alerts`` is a list, so to check to make sure that
    a successful response was retrieved, check using ``alerts[0]``.

    Attributes
    ----------
    total : int or alerts.Error
        The total number of alerts
    land : int or alerts.Error
        The total number of alerts over land
    marine : int or alerts.Error
        The total number of alerts over water
    regions : dict or alerts.Error
        Specifies the number of marine alerts in a certain location (keys: regions, values: int)
    areas : dict or alerts.Error
        Specifies the number of land alerts in a certain location (keys: areas, values: int)
    zones : dict or alerts.Error
        Specifies the number of alerts per zone (keys: zone, values: int)
    """

    # In case there's a bad request or rate limit is hit, these values will be None. Prevents errors
    #   from being raised.
    total = None
    land = None
    marine = None
    regions = None
    areas = None
    zones = None
    alerts = None

    n_errors = 0
    has_any_request_errors = False

    def __repr__(self):
        if not isinstance(self.total, AlertError):
            return self.total

        return self.total.__repr__()

    def __init__(self, user_agent):
        response = utils.request("https://api.weather.gov/alerts/active/count", headers=user_agent)
        self.response_headers = response.headers

        if not response.ok:
            self.total = AlertError(response)
            self.land = AlertError(response)
            self.marine = AlertError(response)
            self.regions = AlertError(response)
            self.areas = AlertError(response)
            self.zones = AlertError(response)
            self.n_errors += 1
            self.has_any_request_errors = True
        else:
            info = response.json()
            self.total = info['total']  # dtype: int
            self.land = info['land']  # dtype: int
            self.marine = info['marine']  # dtype: int
            self.regions = info['regions']  # dtype: dict {str : int}
            self.areas = info['areas']  # dtype: dict {str : int}
            self.zones = info['zones']  # dtype: dict {str : int}

    def _filter_by(self, which_method, filter_item, docs_str) -> dict:
        """Used to refactor filter_x methods. Much cleaner this way."""

        valid = (isinstance(filter_item, str), isinstance(filter_item, list), isinstance(filter_item, tuple))
        if not valid:
            raise ParameterTypeError(filter, "string, list tuple")

        if isinstance(filter_item, str):
            filter_item = [filter_item]  # make it a list to be consistent with logic (eliminates unnecessary if/else)

        if which_method == 'area':
            data_validation = utils.valid_areas()
            self_d = self.areas
        if which_method == 'marine':
            data_validation = ['AL', 'AT', 'GL', 'GM', 'PA', 'PI']
            self_d = self.regions
        if which_method == 'zone':
            data_validation = utils.valid_zones() # Until an entire list is compiled, this won't even execute.
            self_d = self.zones

        filtered_d = {}
        for filter_item in filter_item:  # iterate through user inputs
            filter_item = filter_item.upper()
            if which_method != 'zone': # skip data validation for zone for now.
                if filter_item not in data_validation:
                    raise DataValidationError(filter_item, docs_str)

            if filter_item in self_d: # insert it into the filtered dictionary.
                filtered_d[filter_item] = self_d[filter_item]
            else: # if it doesn't exist in itself, then return 0.
                filtered_d[filter_item] = 0

        return filtered_d

    def filter_marine_regions(self, region: str or list or tuple) -> dict:
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
        return self._filter_by('marine', region,
                               "https://nwsapy.readthedocs.io/en/latest/apiref/alerts/AlertByCount/filter_marine_regions.html")

    def filter_land_areas(self, area: str or list or tuple) -> dict:
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
        return self._filter_by('area', area,
                               "https://nwsapy.readthedocs.io/en/latest/apiref/alerts/AlertByCount/filter_land_areas.html")

    def filter_zones(self, zone: str or list or tuple) -> dict:
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
        return self._filter_by('zone', zone,
                               "https://nwsapy.readthedocs.io/en/latest/apiref/alerts/AlertByCount/filter_zones.html")


class AlertTypes(utils.ObjectIterator):
    r"""A class used to hold information about the alerts types found from ``alerts/types``.

    Attributes
    ----------
    alerts : list or alerts.Error
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    """

    def __init__(self, user_agent):
        response = utils.request("https://api.weather.gov/alerts/types", headers=user_agent)
        if isinstance(response, requests.models.Response):  # successful retrieval.
            self.alerts = response.json()['eventTypes']
        else:
            self.alerts = [response]

        self._iterable = self.alerts  # make it iterable
        self.response_headers = response.headers

    def __repr__(self):
        return ", ".join(self.alerts)


class ServerPing:
    """Tests the server to make sure it's OK."""

    def __init__(self, user_agent):
        response = utils.request("https://api.weather.gov/", headers=user_agent)
        self.status = response.json()['status']
        self.response_headers = response.headers