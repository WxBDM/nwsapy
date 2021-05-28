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
from typing import Union, Optional
import collections
import copy

from shapely.geometry import Point, Polygon
from datetime import datetime
import pandas as pd
import pytz
import numpy as np
import requests

from nwsapy.errors import ParameterTypeError, DataValidationError
import nwsapy.utils as utils


class IndividualAlert:

    def __init__(self, alert_list):
        alert_d = alert_list['properties'] # prep to set all attributes

        # set all attributes
        geom_d = self._format_geometry(alert_list['geometry'])
        alert_d.update(geom_d)

        # set all times
        times = {'sent': alert_d['sent'], 'effective': alert_d['effective'],
                 'onset': alert_d['onset'], 'expires': alert_d['expires'], 'ends': alert_d['ends']}
        time_d = self._set_times(times)
        alert_d.update(time_d)

        # add a pandas series to it, why not?
        alert_d['series'] = self._construct_series(alert_d)

        # fix the affected zones so it's only the zoneID.
        alert_d['affectedZones'] = [zone.split("/")[-1] for zone in alert_d['affectedZones']]
        alert_d['areaDesc'] = alert_d['areaDesc'].split(";")

        for k, v in alert_d.items():
            setattr(self, k, v)

    def _format_geometry(self, geometries):
        if not isinstance(geometries, type(None)):  # if there's any kind of geometry
            # determine the geometry kind. If it's a point, make a list of shapely point objects.
            points = [Point(x[0], x[1]) for x in geometries['coordinates'][0]]
            polygon_d = dict({'points': points})

            # If the geometry type is a polygon, make a polygon object as well. Otherwise set to none.
            geometry_type = geometries['type']
            if geometry_type == 'Polygon':
                polygon_d['polygon'] = Polygon(points)
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

    def _construct_series(self, alert_dictionary):

        # convert from shapely object to lat/lon
        if alert_dictionary['points'] is not None:
            points = [(point.y, point.x) for point in list(alert_dictionary['points'])]  # shapely is backwards >:(
            alert_dictionary['points'] = points

        if alert_dictionary['polygon'] is not None:
            alert_dictionary['polygon'] = list(alert_dictionary['polygon'].exterior.coords)

        series = pd.Series(alert_dictionary)
        return series

    def sent_before(self, other):
        """Method to compare sent times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.sent_utc > other.sent_utc

    def sent_after(self, other):
        """Method to compare sent times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was after before other. False otherwise."""
        return self.sent_utc < other.sent_utc

    def effective_before(self, other):
        """Method to compare effective times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.effective_utc > other.effective_utc

    def effective_after(self, other):
        """Method to compare effective times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was after before other. False otherwise."""
        return self.effective_utc < other.effective_utc

    def onset_before(self, other):
        """Method to compare onset times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.onset_utc > other.onset_utc

    def onset_after(self, other):
        """Method to compare onset times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent after other. False otherwise."""
        return self.onset_utc < other.onset_utc

    def expires_before(self, other):
        """Method to compare expire times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.expires_utc > other.expires_utc

    def expires_after(self, other):
        """Method to compare expire times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent after other. False otherwise."""
        return self.expires_utc < other.expires_utc

    def ends_before(self, other):
        """Method to compare end times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent before other. False otherwise."""
        return self.ends_utc > other.ends_utc

    def ends_after(self, other):
        """Method to compare end times. All times are compared in UTC.

        Returns
        -------
        bool
            True if this alert was sent after other. False otherwise."""
        return self.ends_utc < other.ends_utc


class _AlertIterator:

    def __iter__(self):
        """Allows for iteration though self.alerts."""
        self._alert_index = 0
        return self

    def __next__(self):
        """Allows for iteration through self.alerts."""
        if self._alert_index < len(self.alerts):
            val = self.alerts[self._alert_index]
            self._alert_index += 1
            return val
        else:
            raise StopIteration

    def __getitem__(self, index):
        """Allows for alerts object to be directly indexable."""
        return self.alerts[index]

    def __len__(self):
        return len(self.alerts)


class BaseAlert(_AlertIterator):

    def filter_by(self, alert_id: Optional[Union[str, list[str]]] = None,
                  certainty: Optional[Union[str, list[str]]] = None,
                  effective_after: Optional[datetime] = None,
                  effective_before: Optional[datetime] = None,
                  ends_after: Optional[datetime] = None,
                  ends_before: Optional[datetime] = None,
                  event: Optional[Union[str, list[str]]] = None,
                  expires_after: Optional[datetime] = None,
                  expires_before: Optional[datetime] = None,
                  lat_northern_bound: Optional[Union[float, int]] = None,
                  lat_southern_bound: Optional[Union[float, int]] = None,
                  lon_eastern_bound: Optional[Union[float, int]] = None,
                  lon_western_bound: Optional[Union[float, int]] = None,
                  onset_after: Optional[datetime] = None,
                  onset_before: Optional[datetime] = None,
                  sent_after: Optional[datetime] = None,
                  sent_before: Optional[datetime] = None,
                  severity: Optional[Union[str, list[str]]] = None,
                  status: Optional[Union[str, list[str]]] = None,
                  urgency: Optional[Union[str, list[str]]] = None) -> object:
        r"""Filters all active alerts based upon the alert type.

        Parameters
        ----------
        alert_id: str or list
            The ID associated with a specific alert, or a list containing alerts IDs. If ``None``, this parameter
            is ignored.

        certainty: str or list
            The certainty of the warning. If ``None``, this parameter is ignored. If the attribute is ``None``, the
            alert will be filtered out.

        lat_northern_bound: float or int
            The northern-most latitude in which alerts should be filtered by. For example, if 35 is given, it will
            filter out any alerts that go above 35 latitude. If ``None``, this parameter is ignored. If the attribute
            is ``None``, the alert will be filtered out.

        lat_southern_bound: float or int
            The southern-most latitude in which alerts should be filtered by. For example, if 10 is given, it will
            filter out any alerts that go below 10 latitude. If ``None``, this parameter is ignored. If the attribute
            is ``None``, the alert will be filtered out.

        lon_western_bound: float or int
            The western-most longitude in which alerts should be filtered by. For example, if -100 is given, it will
            filter any alerts that are west of -100 longitude. If ``None``, this parameter is ignored. If the attribute
            is ``None``, the alert will be filtered out.

        lon_eastern_bound: float or int
            The eastern-most longitude in which alerts should be filtered by. For example, if -80 is given, it will
            filter out any alerts that are east of -80 longitude. If ``None``, this parameter is ignored. If the
            attribute is ``None``, the alert will be filtered out.

        effective_before: datetime
            Any effective times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        effective_after: datetime
            Any effective times that are after this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        ends_before: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        ends_after: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        event: str or list
            The event shown on the :ref:`Valid Alert Types<valid_nws_alert_products>` table. If ``None``, this parameter
            is ignored.

        onset_before: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        onset_after: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        sent_before: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        sent_after: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        expires_before: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored.

        expires_after: datetime
            Any end times that are before this parameter will be filtered out. If the attribute is ``None``, it
            will be filtered out. If ``None`` this parameter is ignored. If the two times are equal, they will not be
            filtered out.

        severity: str or list
            The severity in which the alert is. Severity is

        status: Optional[Union[str, list[str]]] = None,

        urgency: Optional[Union[str, list[str]]] = None


        Raises
        ------
        nwsapy.ParameterTypeError
            If the parameter isn't the correct data type.
        nwsapy.DataValidationError
            If the alert type isn't a valid National Weather Service alert.

        Returns
        -------
        self
            A deep copy of the same object, except with the filtered alerts.

        """

        class Params:
            """Class to hold data types and constraints for checking"""

            def __init__(self, param, expected_dtype, constraints, is_list = False):
                if param is not None and is_list:
                    # this guarantees that our values are inside of a list.
                    if not any([isinstance(param, list), isinstance(param, tuple)]):
                        self.value = [param]  # put it into a list so it can be iterated over.
                    else:
                        self.value = param

                    self.dtype = expected_dtype
                else:
                    self.value = None
                    self.dtype = type(None)

                self.constraints = constraints

            def check_data_type(self):
                for itr in self.value:  # iterate through the list (either 1 or n vals)
                    if type(self.dtype) == list:  # some of the parameters have 2 possible dtypes, they're in a list.
                        valid = [isinstance(itr, dtype) for dtype in self.dtype]

                        if not any(valid):
                            raise ParameterTypeError(itr, self.dtype)

                    else:  # otherwise just simply check the data type.
                        if not isinstance(itr, self.dtype):
                            raise ParameterTypeError(itr, self.dtype)

            def validate_data(self):
                if self.constraints is not None:
                    self.value = [x.title() for x in self.value]  # convert all to a string.
                    for val in self.value:
                        if val not in self.constraints:
                            raise DataValidationError(val)

        invalid = [event == [], urgency == [], severity == [], certainty == []]
        if any(invalid):
            raise ParameterTypeError()


        # load the parameters into a dictionary and add their associated data type with it.
        utc_now = type(datetime.utcnow())  # serves no purpose other than to get data type.
        param_d = {
            'alert_id': Params(alert_id, str, None, is_list = True),  # .id
            'certainty': Params(certainty, str, ["Observed", "Likely", "Possible", "Unlikely", "Unknown"],
                                is_list = True),  # certainty
            'effective_after': Params(effective_after, utc_now, None),  # .effective_after
            'effective_before': Params(effective_before, utc_now, None),  # .effective_before
            'ends_after': Params(ends_after, utc_now, None),  # .effective_before
            'ends_before': Params(ends_before, utc_now, None),  # .effective_before
            'event': Params(event, str, utils.valid_products(), is_list = True),  # .event
            'expires_after': Params(expires_after, utc_now, None),  # .expires_after
            'expires_before': Params(expires_before, utc_now, None),  # .expires_before
            'lat_northern_bound': Params(lat_northern_bound, [int, float], None),  # .polygon .point .point_collection
            'lat_southern_bound': Params(lat_southern_bound, [int, float], None),  # .polygon .point .point_collection
            'lon_eastern_bound': Params(lon_eastern_bound, [int, float], None),  # .polygon .point .point_collection
            'lon_western_bound': Params(lon_western_bound, [int, float], None),  # .polygon .point .point_collection
            'onset_after': Params(onset_after, utc_now, None),  # .onset_after
            'onset_before': Params(onset_before, utc_now, None),  # .onset_before
            'sent_after': Params(sent_after, utc_now, None),  # .sent_after
            'sent_before': Params(sent_before, utc_now, None),  # .sent_before
            'severity': Params(severity, str, ["Extreme", "Severe", "Moderate", "Minor", "Unknown"], is_list = True),  # .severity
            'status': Params(status, str, ["Actual", "Exercise", "System", "Test", "Draft"], is_list = True),  # .status
            'urgency': Params(urgency, str, ["Immediate", "Expected", "Future", "Past", "Unknown"], is_list = True),  # .urgency
        }

        # Remove all parameters if it is set to None
        param_iteration_d = copy.deepcopy(param_d)  # need to make a copy of it and iterate through that. RunTimeError.
        for param in param_iteration_d:
            if param_d[param].value is None:
                del param_d[param]

        # Check to see if there were any arguments supplied.
        if len(param_d) == 0:  # there weren't any arguments supplied, throw an error.
            raise ParameterTypeError(filter_by_test=True)

        for param in param_d.values():
            param.check_data_type()   # Check all data types
            param.validate_data()  # Validate the data

        # There's ways to do this, and there's ways to do this efficiently. Clean up at a later point and make more
        #   efficient. Such a hackish way of doing it, but it gets the job done /shrug

        filtered_alerts = []

        if 'alert_id' in param_d:
            value = param_d['alert_id'].value
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.id]

        if 'certainty' in param_d:
            value = param_d['certainty'].value
            filtered_alerts += [alert for v in value for alert in self.alerts
                                if v == alert.certainty]

        if 'effective_after' in param_d:
            value = param_d['effective_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value <= alert.effective])]

        if 'effective_before' in param_d:
            value = param_d['effective_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value >= alert.effective])]

        if 'ends_after' in param_d:
            value = param_d['ends_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value <= alert.ends])]

        if 'ends_before' in param_d:
            value = param_d['ends_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value >= alert.ends])]

        if 'event' in param_d:
            value = param_d['event'].value
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.event]

        if 'expires_after' in param_d:
            value = param_d['expires_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.expires is not None, value <= alert.expires])]

        if 'expires_before' in param_d:
            value = param_d['expires_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.expires is not None, value >= alert.expires])]

        if 'lat_northern_bound' in param_d:
            # self.polygon.bounds => (minx, miny, maxx, maxy)
            value = param_d['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts # check the polygons
                                if all([alert.polygon is not None, value > alert.polygon.bounds[3]])]
            filtered_alerts += [alert for alert in self.alerts # check the points
                                if all([alert.point is not None, value > alert.polygon.bounds[3]])]

        if 'lat_southern_bound' in param_d:
            value = param_d['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts  # check the polygons
                                if all([alert.polygon is not None, value < alert.polygon.bounds[1]])]
            filtered_alerts += [alert for alert in self.alerts  # check the points
                                if all([alert.point is not None, value > alert.point.bounds[1]])]

        if 'lon_eastern_bound' in param_d:
            value = param_d['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts  # check the polygons
                                if all([alert.polygon is not None, value > alert.polygon.bounds[2]])]
            filtered_alerts += [alert for alert in self.alerts  # check the points
                                if all([alert.point is not None, value > alert.point.bounds[2]])]

        if 'lon_western_bound' in param_d:
            value = param_d['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts  # check the polygons
                                if all([alert.polygon is not None, value > alert.polygon.bounds[0]])]
            filtered_alerts += [alert for alert in self.alerts  # check the points
                                if all([alert.point is not None, value > alert.point.bounds[0]])]

        if 'onset_after' in param_d:
            value = param_d['onset_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.onset is not None, value <= alert.onset])]

        if 'onset_before' in param_d:
            value = param_d['onset_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.onset is not None, value >= alert.onset])]

        if 'sent_after' in param_d:
            value = param_d['sent_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.sent is not None, value <= alert.sent])]

        if 'sent_before' in param_d:
            value = param_d['sent_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.sent is not None, value >= alert.sent])]

        if 'severity' in param_d:
            value = param_d['severity'].value
            filtered_alerts += [alert for v in value for alert in self.alerts
                                if v == alert.severity]

        if 'status' in param_d:
            value = param_d['status'].value
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.status]

        if 'urgency' in param_d:
            value = param_d['urgency'].value
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.urgency]

        new_alert_obj = copy.deepcopy(self)
        new_alert_obj.alerts = list(set(filtered_alerts))
        return new_alert_obj

    def to_dataframe(self) -> pd.DataFrame:
        r"""Converts all of all retrieved alerts into a Pandas dataframe.

        Returns
        -------
        pandas.DataFrame
            A dataframe that contains the information (attributes) of all of the alerts requested.
        """
        df = pd.DataFrame()
        for alert in self.alerts:
            df = df.append(alert.series, ignore_index=True) # append the series.

        df = df.fillna(value=np.nan) # in case there is missing data
        return df


@dataclass
class ActiveAlerts(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active``.

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    See Also
    --------
    :ref:`Individual Alerts<individual_alerts_error>`
        These individual alerts comprise of ``alerts.AllAlerts.alerts``.

    """

    def __init__(self, user_agent):

        response = utils.request("https://api.weather.gov/alerts/active", user_agent)

        if isinstance(response, requests.models.Response):
            info = response.json()['features']
            self.alerts = [IndividualAlert(x) for x in info if x['properties']['event'] != 'Test Message']
        else:
            self.alerts = [response]
        self._counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts
        self.response_headers = response.headers  # requests.structures.CaseInsensitiveDict


@dataclass
class AlertById(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/{id}``.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    See Also
    --------
    :ref:`Individual Alerts<individual_alerts_error>`
        These individual alerts comprise of ``alerts.AllAlerts.alerts``.

    """

    def __init__(self, alert_id, user_agent):

        self._validate(alert_id)
        if isinstance(alert_id, str):
            alert_id = [alert_id]  # this is only to make it consistent with logic below.

        self.alerts = []
        self.response_headers = []
        for a_id in alert_id:  # iterate through the alerts
            response = utils.request(f"https://api.weather.gov/alerts/{a_id}", user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)  # if something weird went wrong, put an error response in.
                continue

            info = response.json()  # all is good, construct the alert objects.
            self.alerts.append(IndividualAlert(info))
            self.response_headers.append(response.headers)

        self._counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

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
class AlertByMarineRegion(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/region/{region}``.

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    See Also
    --------
    :ref:`Valid Data Points - Alerts by Marine Region<alerts_by_marine_table_validation>`
        Table in the documentation to show what regions are valid for this function.
    :ref:`Individual Alerts<individual_alerts_error>`
        These individual alerts comprise of ``alerts.AllAlerts.alerts``.

    """

    def __init__(self, region, user_agent):

        self._validate(region)  # make sure the data is valid.

        if isinstance(region, str):
            region = [region]  # make it a list, eliminates unnecessary if/else statements.

        self.alerts = []
        self.response_headers = []
        for region_str in region:
            region_str = region_str.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/region/{region_str}", user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(IndividualAlert(x))
            self.response_headers.append(response.headers)

        self._counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

    def _validate(self, data):

        valid_data = ["AL", "AT", "GL", "GM", "PA", "PI"]

        if isinstance(data, str):
            data = [data]

        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")

            if data_val.upper() not in valid_data:
                raise DataValidationError(data_val)


@dataclass
class AlertByArea(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/area/{area}``.

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    See Also
    --------
    :ref:`Valid Data Points - Alerts by Area Table<alerts_by_area_table_validation>`
        Table in the documentation to show what areas are valid for this function.
    :ref:`Individual Alerts<individual_alerts_error>`
        These individual alerts comprise of ``alerts.AllAlerts.alerts``.

    """

    def __init__(self, area, user_agent):
        self._validate(area)  # make sure the data is valid.

        if isinstance(area, str):
            area = [area]  # make it a list, eliminates unnecessary if/else statements.

        self.alerts = []
        self.response_headers = []
        for area_str in area:
            area_str = area_str.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/area/{area_str}", user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(IndividualAlert(x))

            self.response_headers.append(response.headers)

        self._counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

    def _validate(self, data):

        valid_data = utils.valid_areas()

        if isinstance(data, str):
            data = [data]

        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")

            if data_val.upper() not in valid_data:
                raise DataValidationError(data)


@dataclass
class AlertByCount:
    r"""A class used to hold information about all active alerts found from ``alerts/active/count``

    Note: If successful, all attributes except ``alerts`` will be set to ``None``. If unsuccessful, all attributes
    except ``alerts`` will be set to ``None``. Keep in mind that ``alerts`` is a list, so to check to make sure that
    a successful response was retrieved, check using ``alerts[0]``.

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
    alerts : list
        Used to determine if there was an error with requesting data from the server. See above note.

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

    def __init__(self, user_agent):
        response = utils.request("https://api.weather.gov/alerts/active/count", headers=user_agent)
        self.response_headers = response.headers

        if isinstance(response, requests.models.Response):
            info = response.json()
            self.total = info['total']  # dtype: int
            self.land = info['land']  # dtype: int
            self.marine = info['marine']  # dtype: int
            self.regions = info['regions']  # dtype: dict {str : int}
            self.areas = info['areas']  # dtype: dict {str : int}
            self.zones = info['zones']  # dtype: dict {str : int}
        else:
            self.alerts = [response]

    def _filter_by(self, region_area_or_zone, filter,
                   docs_str) -> dict:  # private method, used to refactor filter_x methods.
        """Used to refactor filter_x methods. Much cleaner this way."""

        valid = (isinstance(filter, str), isinstance(filter, list), isinstance(filter, tuple))
        if not valid:
            raise ParameterTypeError(filter, "string, list tuple")

        if isinstance(filter, str):
            filter = [filter]  # make it a list to be consistent with logic (eliminates unnecessary if/else)

        filtered_d = {}
        for filter_item in filter:  # iterate through user inputs
            filter_item = filter_item.upper()
            if filter_item not in region_area_or_zone.keys():  # ensure that it's in the keys (see __init__)
                raise DataValidationError(filter_item, docs_str)
            filtered_d[filter_item] = region_area_or_zone[filter_item]

        return filtered_d

    def filter_marine_regions(self, region: Union[str, list, tuple]) -> dict:
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
        return self._filter_by(self.regions, region,
                               "https://nwsapy.readthedocs.io/en/latest/apiref/alerts/AlertByCount/filter_marine_regions.html")

    def filter_land_areas(self, area: Union[str, list, tuple]) -> dict:
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
        return self._filter_by(self.areas, area,
                               "https://nwsapy.readthedocs.io/en/latest/apiref/alerts/AlertByCount/filter_land_areas.html")

    def filter_zones(self, zone: Union[str, list, tuple]) -> dict:
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
        return self._filter_by(self.zones, zone,
                               "https://nwsapy.readthedocs.io/en/latest/apiref/alerts/AlertByCount/filter_zones.html")


@dataclass
class AllAlerts(BaseAlert):
    r"""A class used to hold information about all alerts found from ``alerts/active``.

    Attributes
    ----------
    alerts : list
        A list containing alerts (data type: the alert name) corresponding to the alert.
        Example: [alert.tornadowarning, alert.testmessage, alert.smallcraftadvisory, ...]
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    See Also
    --------
    :ref:`Individual Alerts`<individual_alerts_error>`
        These individual alerts comprise of ``alerts.AllAlerts.alerts``.

    """

    def __init__(self, user_agent):
        response = utils.request("https://api.weather.gov/alerts", headers=user_agent)

        if isinstance(response, requests.models.Response):  # successful retrieval
            info = response.json()['features']
            self.alerts = [IndividualAlert(x) for x in info if x['properties']['event'] != 'Test Message']
        else:
            self.alerts = [response]

        self._counter = collections.Counter(x.event for x in self.alerts)
        self.response_headers = response.headers


@dataclass
class AlertTypes(_AlertIterator):
    r"""A class used to hold information about the alerts types found from ``alerts/types``.

    Attributes
    ----------
    alerts : list
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

        self.response_headers = response.headers

    def __repr__(self):
        return ", ".join(self.alerts)


@dataclass
class AlertByZone(BaseAlert):
    r"""A class used to hold information about all active alerts found from ``alerts/active/zone/{zoneId}``.

    Each alert is it's own object type that is stored in a list (``self.alerts``). That is:
        A tornado warning alert would be a tornadowarning object.

        A small craft advisory alert would be a smallcraftadvisory object.

    Attributes
    ----------
    alerts : list
        A list containing data types corresponding to the alert.
    response_headers : requests.structures.CaseInsensitiveDict
        A dictionary containing the response headers.

    Note
    ----
    This does not have data validation checks, so ensure that your zone ID's are correct, otherwise
    you may run into a 404 error.

    See Also
    --------
    :ref:`Individual Alerts<individual_alerts_error>`
        These individual alerts comprise of ``alerts.AllAlerts.alerts``.

    """

    def __init__(self, zoneID, user_agent):

        self._validate(zoneID)  # make sure the data is valid.

        if isinstance(zoneID, str):
            zoneID = [zoneID]  # make it a list, eliminates unnecessary if/else statements.

        self.alerts = []
        self.response_headers = []
        for zone in zoneID:
            zone = zone.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/zone/{zone}", headers=user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(IndividualAlert(x))
            self.response_headers.append(response.headers)

        self._counter = collections.Counter(x.event for x in self.alerts)  # counts the number of alerts

    def _validate(self, data):

        if isinstance(data, str):
            data = [data]

        for data_val in data:
            if not isinstance(data_val, str):
                raise ParameterTypeError(data_val, "string")


class ServerPing:

    def __init__(self, user_agent):
        response = utils.request("https://api.weather.gov/", headers=user_agent)
        self.status = response.json()['status']
        self.response_headers = response.headers
