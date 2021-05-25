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
from typing import Union, Optional, Dict, Any
import collections
import copy

from shapely.geometry import Point, Polygon, MultiPoint
from datetime import datetime
import pandas as pd
import pytz
import numpy as np
import requests

from nwsapy.errors import ParameterTypeError, DataValidationError, ParameterConflict
import nwsapy.utils as utils


class AlertConstructor:
    """Constructs the individual alert object."""

    def construct_alert(self, alert_list):
        alert_dictionary = alert_list['properties']
        if not isinstance(alert_list['geometry'], type(None)):
            alert_dictionary.update({'geometry': alert_list['geometry']})
            self._construct_geometry(alert_dictionary)  # even though the dict is being updated, it returns nothing.
        else:  # there's no geometry tag, so make them none.
            no_geometry = dict({"points": None, 'polygon': None, "points_collection": None})  # set to none
            alert_dictionary.update(no_geometry)

        if 'geometry' in alert_dictionary.keys():
            del alert_dictionary['geometry']  # get rid of this, it's not needed (shapely)

        self._construct_times(alert_dictionary)
        constructed_alert = self._construct_methods(alert_dictionary)
        constructed_alert.series = self._construct_series(alert_dictionary)

        # set the comparison times to start.
        constructed_alert._time_compare = constructed_alert.sent

        # fix the affected zones so it's only the zoneID.
        constructed_alert.affectedZones = [zone.split("/")[-1] for zone in constructed_alert.affectedZones]
        return constructed_alert()

    def _construct_series(self, alert_dictionary):

        # convert from shapely object to lat/lon
        if alert_dictionary['points'] is not None:
            points = [(point.y, point.x) for point in list(alert_dictionary['points'])]  # shapely is backwards >:(
            alert_dictionary['points'] = points

        if alert_dictionary['polygon'] is not None:
            alert_dictionary['polygon'] = list(alert_dictionary['polygon'].exterior.coords)

        series = pd.Series(alert_dictionary)
        series = series.drop(labels=['points_collection'])
        return series

    def _construct_methods(self, alert_dictionary):
        """Constructs the object's methods and returns it."""

        # these methods are ones that are going to be bound to the object.
        # Leaving here for backwards compatability.
        def sent_before(self, other):
            return self.sent > other.sent

        def sent_after(self, other):
            return self.sent < other.sent

        def effective_before(self, other):
            return self.effective > other.effective

        def effective_after(self, other):
            return self.effective < other.effective

        def onset_before(self, other):
            return self.onset > other.onset

        def onset_after(self, other):
            return self.onset < other.onset

        def expires_before(self, other):
            return self.expires > other.expires

        def expires_after(self, other):
            return self.expires < other.expires

        def ends_before(self, other):
            return self.ends > other.ends

        def ends_after(self, other):
            return self.ends < other.ends

        def set_time_comparison(self, which):  # sets the value to compare the time to for __lt__ etc.
            which = which.lower()
            if which not in ['effective', 'sent', 'onset', 'expires', 'ends']:
                raise DataValidationError(which, "Valid parameters: 'effective', 'sent', 'onset', 'expires', 'ends'")

            if which == 'effective':
                self._time_compare = self.effective
            elif which == 'sent':
                self._time_compare = self.sent
            elif which == 'onset':
                self._time_compare = self.onset
            elif which == 'expires':
                self._time_compare = self.expires
            else:
                self._time_compare = self.expires

        # methods to compare times.
        def __lt__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.__hash__ < other.__hash__

        def __le__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.__hash__ <= other.__hash__

        def __eq__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.id == other.id

        def __ne__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.__hash__ != other.__hash__

        def __gt__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.__hash__ > other.__hash__

        def __ge__(self, other):
            if not isinstance(other, type(self)): return NotImplemented
            return self.__hash__ >= other.__hash__

        # other dunder methods
        def __repr__(self):
            return self.headline

        def __hash__(self):
            return hash((self.id,))

        # Create the object and bind the method to it.
        alert = type(alert_dictionary['event'].replace(" ", "").lower(), (), alert_dictionary)
        alert.sent_before = MethodType(sent_before, alert)
        alert.sent_after = MethodType(sent_after, alert)
        alert.effective_before = MethodType(effective_before, alert)
        alert.effective_after = MethodType(effective_after, alert)
        alert.onset_before = MethodType(onset_before, alert)
        alert.onset_after = MethodType(onset_after, alert)
        alert.expires_before = MethodType(expires_before, alert)
        alert.expires_after = MethodType(expires_after, alert)
        alert.ends_before = MethodType(ends_before, alert)
        alert.ends_after = MethodType(ends_after, alert)
        alert.__lt__ = MethodType(__lt__, alert)
        alert.__le__ = MethodType(__le__, alert)
        alert.__eq__ = MethodType(__eq__, alert)
        alert.__ne__ = MethodType(__ne__, alert)
        alert.__gt__ = MethodType(__gt__, alert)
        alert.__ge__ = MethodType(__ge__, alert)
        alert.__repr__ = MethodType(__repr__, alert)
        alert.__hash__ = MethodType(__hash__, alert)
        alert.set_time_comparison = MethodType(set_time_comparison, alert)

        return alert  # we're not instantiating the object here. It's in the main construct method.

    def _construct_geometry(self, alert_dictionary):

        """Construct alert.polygon, alert.points, and alert.multipoint"""
        # determine the geometry kind. If it's a point, make a list of shapely point objects, and create a multipoint
        # object.

        # If there is a geometry, then make points and points collection at a minimum.
        geometry_type = alert_dictionary['geometry']['type']
        points = [Point(x[0], x[1]) for x in alert_dictionary['geometry']['coordinates'][0]]
        polygon_d = dict({'points': points, 'points_collection': MultiPoint(points)})

        # If the geometry type is a polygon, make a polygon object as well. Otherwise set to none.
        if geometry_type == 'Polygon':
            polygon_d['polygon'] = Polygon(points)
        else:  # only if it's a point (just in case, this needs to be tested)
            polygon_d['polygon'] = None

        alert_dictionary.update(polygon_d)

    def _construct_times(self, alert_dictionary):
        # convert times to a date time object.
        all_times = ['sent', 'effective', 'onset', 'expires', 'ends']
        for time in all_times:
            if not isinstance(alert_dictionary[time], type(None)):
                alert_dictionary[time] = datetime.fromisoformat(alert_dictionary[time])


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

    def _validate_alert_type(self, alert_type: Union[str, list]):

        # checks to make sure that the data type is correct and is validated against the various alert types.

        invalid = (isinstance(alert_type, str), isinstance(alert_type, list), isinstance(alert_type, tuple))
        if not any(invalid):  # if it's not string, list, or tuple
            raise ParameterTypeError(alert_type, 'string, list, or tuple')

        if isinstance(alert_type, str):
            alert_type = [alert_type]

        # make sure it's a valid product. If so, then we're okay to check inside of the collections.
        valid_products = utils.valid_products()  # Update this list on an as-needed basis. No need to ping server.
        for alert in alert_type:
            if alert.title() not in valid_products:
                raise DataValidationError(alert)

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
        event: str or list
            The event shown on the :ref:`Valid Alert Types<valid_nws_alert_products>` table. If ``None``, this parameter
            is ignored.

        alert_id: str or list
            The ID associated with a specific alert, or a list containing alerts IDs. If ``None``, this parameter
            is ignored.

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
        nwsapy.ParameterConflict
            If the parameters have a conflict with one another. Only set one of the following: region_type
            point region zone area.

        Returns
        -------
        self
            A deep copy of the same object, except with the filtered alerts.

        """

        class Params:
            """Class to hold data types and constraints for checking"""

            def __init__(self, param, expected_dtype, constraints):
                if param is not None:
                    if not any([isinstance(param, list), isinstance(param, tuple)]):
                        self.value = [param]
                    else:
                        self.value = param

                    self.dtype = expected_dtype
                else:
                    self.value = None
                    self.dtype = type(None)

                self.constraints = constraints

            def title(self):
                if self.value is not None:
                    self.value = [x.title() for x in self.value]  # convert all to a string.

        # load the parameters into a dictionary and add their associated data type with it.
        # Note: don't call any string modification methods in initialization, it messes up the tests.
        utc_now = type(datetime.utcnow())  # serves no purpose other than to get data type.
        param_d = {
            'alert_id': Params(alert_id, str, None),  # .id
            'certainty': Params(certainty, str, ["Observed", "Likely", "Possible", "Unlikely", "Unknown"]),  # certainty
            'effective_after': Params(effective_after, utc_now, None),  # .effective_after
            'effective_before': Params(effective_before, utc_now, None),  # .effective_before
            'ends_after': Params(ends_after, utc_now, None),  # .effective_before
            'ends_before': Params(ends_before, utc_now, None),  # .effective_before
            'event': Params(event, str, utils.valid_products()),  # .event
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
            'severity': Params(severity, str, ["Extreme", "Severe", "Moderate", "Minor", "Unknown"]),  # .severity
            'status': Params(status, str, ["Actual", "Exercise", "System", "Test", "Draft"]),  # .status
            'urgency': Params(urgency, str, ["Immediate", "Expected", "Future", "Past", "Unknown"]),  # .urgency
        }

        # This checks 3 things:
        #   1. If there is at least one filter argument supplied.
        #   2. If the data type of the filter argument is as expected
        #   3. If the data is validated (is of proper kind)
        # clean up, it's unfun to read. Yikes!
        args_supplied = {}  # list of all of the arguments that are supplied.
        for key in param_d:  # iterate through entire parameter dictionary
            val = param_d[key]  # set the value (Params object)
            if not isinstance(val.value, type(None)):  # point 2: check if it's None. If not, move on.
                args_supplied.update({key: val})  # put it in the argument supplied dictionary.

                for itr in val.value:  # iterate thorugh the list (either 1 or n vals)
                    if type(val.dtype) == list:  # some of the parameters have 2 possible dtypes, they're in a list.
                        valid = [isinstance(itr, dtype) for dtype in val.dtype]
                        if not any(valid):
                            raise ParameterTypeError(itr, 'int or float')  # just hardcode it for now watch scalability
                    else:  # otherwise just simply check the data type.
                        if not isinstance(itr, val.dtype):
                            raise ParameterTypeError(itr, val.dtype)

                # Point 3
                if val.constraints is not None:
                    val.title()
                    value = val.value  # there could be filters where it's a list, so convert it to a list.
                    for itr_val in value:
                        if itr_val not in val.constraints:
                            raise DataValidationError(value)

        if len(args_supplied) == 0:  # there weren't any arguments supplied, throw an error.
            raise ParameterTypeError(filter_by_test=True)

        # There's ways to do this, and there's ways to do this efficiently. Clean up at a later point and make more
        #   efficient. Such a hackish way of doing it, but it gets the job done /shrug

        filtered_alerts = []

        if 'alert_id' in args_supplied:
            value = args_supplied['alert_id'].value
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.id]

        if 'certainty' in args_supplied:
            value = args_supplied['certainty'].value
            filtered_alerts += [alert for v in value for alert in self.alerts
                                if v == alert.certainty]

        if 'effective_after' in args_supplied:
            value = args_supplied['effective_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value <= alert.effective])]

        if 'effective_before' in args_supplied:
            value = args_supplied['effective_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value >= alert.effective])]

        if 'ends_after' in args_supplied:
            value = args_supplied['ends_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value <= alert.ends])]

        if 'ends_before' in args_supplied:
            value = args_supplied['ends_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.effective is not None, value >= alert.ends])]

        if 'event' in args_supplied:
            value = args_supplied['event'].value
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.event]

        if 'expires_after' in args_supplied:
            value = args_supplied['expires_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.expires is not None, value <= alert.expires])]

        if 'expires_before' in args_supplied:
            value = args_supplied['expires_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.expires is not None, value >= alert.expires])]

        if 'lat_northern_bound' in args_supplied:
            # self.polygon.bounds => (minx, miny, maxx, maxy)
            value = args_supplied['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts # check the polygons
                                if all([alert.polygon is not None, value > self.polygon.bounds[3]])]
            filtered_alerts += [alert for alert in self.alerts # check the points
                                if all([alert.point is not None, value > self.polygon.bounds[3]])]

        if 'lat_southern_bound' in args_supplied:
            value = args_supplied['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts  # check the polygons
                                if all([alert.polygon is not None, value < self.polygon.bounds[1]])]
            filtered_alerts += [alert for alert in self.alerts  # check the points
                                if all([alert.point is not None, value > self.point.bounds[1]])]

        if 'lon_eastern_bound' in args_supplied:
            value = args_supplied['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts  # check the polygons
                                if all([alert.polygon is not None, value > self.polygon.bounds[2]])]
            filtered_alerts += [alert for alert in self.alerts  # check the points
                                if all([alert.point is not None, value > self.point.bounds[2]])]
        if 'lon_western_bound' in args_supplied:
            value = args_supplied['lat_northern_bound'].value
            filtered_alerts += [alert for alert in self.alerts  # check the polygons
                                if all([alert.polygon is not None, value > self.polygon.bounds[0]])]
            filtered_alerts += [alert for alert in self.alerts  # check the points
                                if all([alert.point is not None, value > self.point.bounds[0]])]

        if 'onset_after' in args_supplied:
            value = args_supplied['onset_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.onset is not None, value <= alert.onset])]

        if 'onset_before' in args_supplied:
            value = args_supplied['onset_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.onset is not None, value >= alert.onset])]

        if 'sent_after' in args_supplied:
            value = args_supplied['sent_after'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.sent is not None, value <= alert.sent])]

        if 'sent_before' in args_supplied:
            value = args_supplied['sent_before'].value
            filtered_alerts += [alert for alert in self.alerts
                                if all([alert.sent is not None, value >= alert.sent])]

        if 'severity' in args_supplied:
            value = args_supplied['severity'].value
            if type(value) != list:
                value = [value]
            filtered_alerts += [alert for v in value for alert in self.alerts
                                if v == alert.severity]

        if 'status' in args_supplied:
            value = args_supplied['status'].value
            if type(value) != list:
                value = [value]
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.status]

        if 'urgency' in args_supplied:
            value = args_supplied['urgency'].value
            if type(value) != list:  # yuck
                value = [value]
            filtered_alerts += [alert for v in value for alert in self.alerts if v == alert.urgency]

        new_alert_obj = copy.deepcopy(self)
        new_alert_obj.alerts = list(set(filtered_alerts))
        return new_alert_obj

    def count(self, alert_type: Union[str, list]) -> Union[int, list]:
        r"""A method to give you the number of alerts of a specific type that are active.

        Parameters
        ----------
        alert_type : str, list
            The type of alert to be searched. Not case sensitive. Examples: ``Tornado Warning``, ``flood watch``.
            If it's a list, it will return a list of the number of warnings in the order it's provided. For example,
            ``count(['Tornado Warning', 'Freeze Warning'])`` will return the number of tornado warnings
            and the number of freeze warnings (e.g. ``[1, 10]``).

        Raises
        ------
        nwsapy.ParameterTypeError
            If the parameter isn't the correct data type (string).
        nwsapy.DataValidationError
            If the alert type isn't a valid National Weather Service alert.
            See: :ref:`Valid Alert Types<valid_nws_alert_products>`

        Returns
        -------
        int, list
            The number of alerts that are of the alert type. If a list, the number of alerts in order of the parameter.

        """
        self._validate_alert_type(alert_type)  # validate data
        if isinstance(alert_type, str):
            alert_type = [alert_type]  # this is only to make it consistent with logic below.

        # it's valid, get it from the counter.
        count = [self._counter[alert.title()] if alert.title() in self._counter else 0 for alert in alert_type]
        if len(count) == 1:  # if there's only one alert type that was given.
            return count[0]
        if len(count) == 0:  # if there's zero, then give 0.
            return 0

        return count  # otherwise, return the list.

    def to_dataframe(self) -> pd.DataFrame:
        r"""Converts all of all retrieved alerts into a Pandas dataframe.

        Returns
        -------
        pandas.DataFrame
            A dataframe that contains the information (attributes) of all of the alerts requested.
        """

        df = pd.DataFrame()
        for alert in self.alerts:
            df = df.append(alert.series, ignore_index=True)

        df = df.fillna(value=np.nan)
        return df

    def as_utc_time(self):
        """Sets the object's datetime objects to UTC time.

        Caution
        -------
        The alert object does **not** store the original timezone, so if you need to convert back to the timezone of
        issuance, you will be unable to.

        Returns
        -------
        self
            A deep copy of the same object, except with the times converted to UTC.
        """

        # TODO: change series to reflect utc times.

        new_alert_obj = copy.deepcopy(self)
        utc = pytz.timezone("UTC")

        # convert it to UTC from local time.
        for index, alert in enumerate(self.alerts):  # future update: clean this up. too many if's
            if not isinstance(alert.effective, type(None)):
                new_alert_obj[index].effective = alert.effective.astimezone(utc)
            if not isinstance(alert.sent, type(None)):
                new_alert_obj[index].sent = alert.sent.astimezone(utc)
            if not isinstance(alert.onset, type(None)):
                new_alert_obj[index].onset = alert.onset.astimezone(utc)
            if not isinstance(alert.expires, type(None)):
                new_alert_obj[index].expires = alert.expires.astimezone(utc)
            if not isinstance(alert.ends, type(None)):
                new_alert_obj[index].ends = alert.ends.astimezone(utc)

        return new_alert_obj


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

        # Update for 0.2.0: allow users to input values to modify the URL. Lots of checking!

        # active = boolean
        # start_time = datetime object TO 2021-05-19T10:45:00-05:00 (https://en.m.wikipedia.org/wiki/ISO_8601#Durations)
        # end_time = datetime object TO ISO duration (above)
        # status = string [actual, exercise, system, test, draft]
        # message_type = string [alert, update, cancel]
        # event = string [Valid NWS alert products, see table]
        # code = string (no clue what this is)
        # region_type = string [land or marine], This parameter is incompatible with the following parameters:
        #       area, point, region, zone
        # point = string (NOTE: must be 38,-99 WATCH SPACES!, truncate to 4 decimal places).
        #       maybe make a shapely point? OR could create a NWSAPy point. This parameter is incompatible with the
        #       following parameters: area, region, region_type, zone
        # region = string [Valid marine regions, see table] This parameter is incompatible with the following
        #       parameters: area, point, region_type, zone
        # area = string [Valid areas, see table] This parameter is incompatible with the following parameters:
        #       point, region, region_type, zone
        # zone = string [Don't have a table for this, but something like ABC001] This parameter is incompatible with
        #       the following parameters: area, point, region, region_type
        # urgency = string  [immediate, expected, future, past, unknown]
        # severity = string [extreme, severe, moderate, minor, unknown]
        # certainty = string [observed, likely, possible, unlikely, unknown]
        # limit = integer (how many alerts you want, 0 to ??, look into capping it?)
        # cursor = what is this I don't even know

        response = utils.request("https://api.weather.gov/alerts/active", user_agent)

        if isinstance(response, requests.models.Response):
            info = response.json()['features']
            ac = AlertConstructor()
            self.alerts = [ac.construct_alert(x) for x in info]  # opted for list comp because it's faster
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
        ac = AlertConstructor()
        for a_id in alert_id:  # iterate through the alerts
            response = utils.request(f"https://api.weather.gov/alerts/{a_id}", user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)  # if something weird went wrong, put an error response in.
                continue

            info = response.json()  # all is good, construct the alert objects.
            self.alerts.append(ac.construct_alert(info))
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
        ac = AlertConstructor()
        for region_str in region:
            region_str = region_str.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/region/{region_str}", user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(ac.construct_alert(x))
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
        ac = AlertConstructor()
        for area_str in area:
            area_str = area_str.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/area/{area_str}", user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(ac.construct_alert(x))

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
            ac = AlertConstructor()
            self.alerts = [ac.construct_alert(x) for x in info]
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
        ac = AlertConstructor()
        for zone in zoneID:
            zone = zone.upper()
            response = utils.request(f"https://api.weather.gov/alerts/active/zone/{zone}", headers=user_agent)
            if not isinstance(response, requests.models.Response):
                self.alerts.append(response)
                continue

            info = response.json()['features']
            for x in info:
                self.alerts.append(ac.construct_alert(x))
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
