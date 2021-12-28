# General file structure:
#   Request error object
#   Individual components of the module
#   Base endpoint
#   All endpoints associated with /path/to/endpoint

import shapely
from shapely.geometry import Point
from datetime import datetime
import pandas as pd
import pytz
import numpy as np

from nwsapy.core.inheritance.request_error import RequestError
from nwsapy.core.inheritance.base_endpoint import BaseEndpoint
from nwsapy.core.errors import KwargValidationError
from nwsapy.core.validation import DataValidationChecker
from nwsapy.core.url_constructor import construct_active_alert_url as construct_url

class IndividualAlert:
    def __init__(self, alert_list):
        # These need to get updated, tjhey're not parameters - they're attributes.ß
        """Individual alert class, holds properties describing each individual 
        alert.
        
        :param affectedZones: A list of affected zones by ID.
        :type affectedZones: list[str]
        :param areaDesc: A description of the area that the alert covers.
        :type areaDesc: str
        :param category: The category in which the alert falls under.
        :type category: str
        :param description: Describes the alert.
        :type description: str
        :param effective: When the alert is effective (local time)
        :type effective: datetime.datetime
        :param effective_utc: When the alert is effective (local time)
        :type effective_utc: datetime.datetime
        :param ends: When the alert ends (local time)
        :type ends: datetime.datetime or None
        :param ends_utc: When the alert ends (UTC time)
        :type ends_utc: datetime.datetime or None
        :param event: The event of which this alert is (used as the object type)
        :type event: str
        :param expires: When the alert ends (local time)
        :type expires: datetime.datetime or None
        :param expires_utc: When the alert ends (UTC time)
        :type expires_utc: datetime.datetime or None
        :param geocode: 
        :type geocode: dict
        :param headline: The headline of the alert.
        :type headline: str
        :param id: The associated ID of the alert.
        :type id: str
        :param instruction: The “call to action” of the alerrt.
        :type instruction: str
        :param messageType: What kind of message the alert is (update, warning, etc)
        :type messageType: str
        :param onset: When the alert was onset (local time).
        :type onset: datetime.datetime
        :param onset_utc: When the alert was onset (UTC time).
        :type onset_utc: datetime.datetime
        :param parameters: 
        :type parameters: dict
        :param points: Points where the alert lies (lat/lon)
        :type points: list, containing shapely.Point or None
        :param polygon: The polygon where the alert lies.
        :type polygon: shapely.Polygon or None
        :param references: 
        :type references: list
        :param sender: Who sent the alert.
        :type sender: str
        :param senderName: Which NWS office sent the alert.
        :type senderName: str
        :param sent: When the alert was sent (local time)
        :type sent: datetime.datetime
        :param sent_utc: When the alert was sent (UTC time)
        :type sent_utc: datetime.datetime
        :param series: A pandas series with all attributes of this object
        :type series: pandas.Series
        :param severity: The severity level of the alert.
        :type severity: str
        :param status: The status level of the alert.
        :type status: str
        :param urgency: The urgency level of the alert.
        :type urgency: str
        """
        alert_d = alert_list['properties'] # prep to set all attributes

        # set all attributes, starting with geometry.
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

        # set the attributes for the class.
        for k, v in alert_d.items():
            setattr(self, k, v)

        # used for to_dict(). __dict__ doesn't get class variables.
        self._d = alert_d

    def _format_geometry(self, geometries):
        
        # if there's any kind of geometry
        if not isinstance(geometries, type(None)): 
            geometry_type = geometries['type']

            # First check to see if it's a multipolygon. 
            # If so, then create polygons out of it.
            if geometry_type == "MultiPolygon":
                points = []
                polygons = []
                for polygon in geometries['coordinates']:
                    polygon_points = [Point(x[0], x[0]) for x in polygon[0]]
                    points.append(polygon_points)
                    polygons.append(shapely.geometry.Polygon(polygon_points))

                return dict({"points" : points, "polygon" : polygons})

            # determine the geometry kind. If it's a point, make a list of 
            # shapely point objects.
            points = [Point(x[0], x[1]) for x in geometries['coordinates'][0]]
            polygon_d = dict({'points': points})

            # If the geometry type is a polygon, make a polygon object as well. 
            # Otherwise set to none.
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
        
        # iterate through the dictionary of times.      
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

        :return: A dictionary containing all of the attributes of the object.
        :rtype: dict
        """
        return self._d

    def sent_before(self, other):
        """Method to compare sent times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert was sent before ``other``.
        :rtype: bool
        """
        return self.sent_utc > other.sent_utc

    def sent_after(self, other):
        """Method to compare sent times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert was after before ``other``.
        :rtype: bool
        """
        return self.sent_utc < other.sent_utc

    def effective_before(self, other):
        """Method to compare effective times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert was effective before ``other``.
        :rtype: bool
        """
        return self.effective_utc > other.effective_utc

    def effective_after(self, other):
        """Method to compare effective times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert was effective after ``other``.
        :rtype: bool
        """
        return self.effective_utc < other.effective_utc

    def onset_before(self, other):
        """Method to compare onset times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert was onset before ``other``.
        :rtype: bool
        """
        return self.onset_utc > other.onset_utc

    def onset_after(self, other):
        """Method to compare onset times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert was onset after ``other``.
        :rtype: bool
        """
        return self.onset_utc < other.onset_utc

    def expires_before(self, other):
        """Method to compare expire times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert expires before ``other``.
        :rtype: bool
        """
        return self.expires_utc > other.expires_utc

    def expires_after(self, other):
        """Method to compare expire times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert expires before ``other``.
        :rtype: bool
        """
        return self.expires_utc < other.expires_utc

    def ends_before(self, other):
        """Method to compare end times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert ends before ``other``.
        :rtype: bool
        """
        return self.ends_utc > other.ends_utc

    def ends_after(self, other):
        """Method to compare end times. All times are compared in UTC.

        :param other: Another individual alert object.
        :type other: alerts.IndividualAlert
        :return: True if the alert ends after ``other``.
        :rtype: bool
        """
        return self.ends_utc < other.ends_utc


class ActiveAlert(BaseEndpoint):
    
    # Copy/Paste these values for each base method that is a "passthrough".
    _to_df_implement = False
    _to_pint_implement = False
    _to_dict_implement = False
    
    def __init__(self, user_agent, **kwargs):
        super(BaseEndpoint, self).__init__()
        
        dvt = DataValidationChecker()
        dvt.check_parameters(kwargs)
        
        url = construct_url(kwargs)
        response = self._request_api(url, user_agent)
        
        if self.has_any_request_errors:
            self.values = RequestError(response)
        else:
            self.values = 'CHANGE ME BECAUSE IT WILL VARY ACROSS ENDPOINTS'
        
        self._set_iterator(self.values)
    