# General file structure:
#   Request error object
#   Individual components of the module
#   Base endpoint
#   All endpoints associated with /path/to/endpoint

import shapely
from shapely.geometry import Point
from datetime import datetime
from collections import OrderedDict
from warnings import warn
import pandas as pd
import pytz
import numpy as np

from nwsapy.core.inheritance.base_endpoint import BaseEndpoint

class IndividualAlert:
    def __init__(self, alert_list):
        # These need to get updated, tjhey're not parameters - they're attributes.ß
        """Individual alert class, holds properties describing each individual 
        alert. The attributes are as follows:
        
        affectedZones: A list of affected zones by ID. Type: list[str]
        areaDesc: A description of the area that the alert covers. Type: str
        category: The category in which the alert falls under. Type: str
        description: Describes the alert. Type: str
        effective: When the alert is effective (local time). Type: datetime.datetime
        effective_utc: When the alert is effective (local time). Type: datetime.datetime
        ends: When the alert ends (local time). Type: datetime.datetime or None
        ends_utc: When the alert ends (UTC time). Type: datetime.datetime or None
        event: The event of which this alert is (used as the object type) Type: tr
        expires: When the alert ends (local time). Type: datetime.datetime or None
        expires_utc: When the alert ends (UTC time). Type: datetime.datetime or None
        geocode: Unknown. Type: dict
        headline: The headline of the alert. Type: str
        id: The associated ID of the alert. Type: str
        instruction: The “call to action” of the alert. Type: str
        messageType: What kind of message the alert is (update, warning, etc). Type: str
        onset: When the alert was onset (local time). Type: datetime.datetime
        onset_utc: When the alert was onset (UTC time). Type: datetime.datetime
        parameters: Unknown. Type: dict
        points: Points where the alert lies (lat/lon). Type: list, containing shapely.Point or None
        polygon: The polygon where the alert lies. Type: shapely.Polygon or None
        references: Unknown. Type: list
        sender: Who sent the alert. Type:str
        senderName: Which NWS office sent the alert. Type: senderName: str
        sent: When the alert was sent (local time). Type: datetime.datetime
        sent_utc: When the alert was sent (UTC time). Type: datetime.datetime
        series: A pandas series with all attributes of this object. Type: pandas.Series
        severity: The severity level of the alert. Type: str
        status: The status level of the alert. Type: str
        urgency: The urgency level of the alert. Type: str
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
        alert_d['affected_zones'] = [zone.split("/")[-1] for zone in alert_d['affectedZones']]
        alert_d['area_desc'] = alert_d['areaDesc'].split(";")
        alert_d['message_type'] = alert_d['messageType']
        alert_d['sender_name'] = alert_d['senderName']

        # set the attributes for the class.
        for k, v in alert_d.items():
            setattr(self, k, v)

        # used for to_dict(). __dict__ doesn't get class variables.
        self._d = alert_d
        
        self._series = pd.Series(data = self._d)

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

class BaseAlert(BaseEndpoint):
    
    def __init__(self):
        super(BaseEndpoint, self).__init__()
        
    def to_dict(self):
        """Returns the alerts in a dictionary format, where the keys are numbers
        which map to an individual alert.

        :return: Dictionary containing the values of the active alerts.
        :rtype: dict
        """
        # in case it's an error (i.e. correlationid is in it)
        if isinstance(self.values, dict):
            return self.values

        # otherwise, create a new dictionary to reformat it and make it look
        # better.
        d = {}
        for index, alert in enumerate(self.values):
            d[index + 1] = alert.to_dict()
        
        return d
    
    def to_df(self):
        """Returns the values of the alerts in a pandas dataframe structure.

        :return: Dataframe of the values of the alerts.
        :rtype: pandas.DataFrame
        """
        # if it's an error
        if isinstance(self.values, dict):
            return pd.DataFrame(data = self.values)
        
        # Performance issue: appending to a dataframe. This isn't ideal, so 
        # solution to this is found here:
        #   https://stackoverflow.com/questions/27929472/improve-row-append-performance-on-pandas-dataframes
        # ... it's a lot faster, wow.
        
        d = OrderedDict()
        
        # self.values index is arbitrary.
        for index, individual_alert in enumerate(self.values):
            d[index] = individual_alert._d
        
        df = pd.DataFrame.from_dict(d).transpose()
        df = df.reindex(sorted(df.columns), axis = 1) # alphabetize columns.
        df = df.fillna(value = np.nan)
        return df

class ActiveAlerts(BaseAlert):
    
    def __init__(self):
        super(BaseAlert, self).__init__()

class Alerts(BaseAlert):
    
    def __init__(self):
        super(BaseAlert, self).__init__()

class AlertById(BaseAlert):
    
    def __init__(self):
        super(BaseAlert, self).__init__()

class AlertByArea(BaseAlert):
    
    def __init__(self):
        super(BaseAlert, self).__init__()
        
class AlertByZone(BaseAlert):
    
    def __init__(self):
        super(BaseAlert, self).__init__()

class AlertByMarineRegion(BaseAlert):
    
    def __init__(self):
        super(BaseAlert, self).__init__()

class AlertByType(BaseEndpoint):
    
    def __init__(self):
        super(BaseEndpoint, self).__init__()

class AlertCount(BaseEndpoint):
    
    def __init__(self):
        super(BaseEndpoint, self).__init__()
    
    def to_dict(self):
        return self.values

    # The dataframe method could get pretty interesting. There's a few different
    # ways that it could be implemented, but for the sake of v1.0.0, this
    # method is left out.
    
    # Figure out what these methods do in the original package.
    def filter_zones(self, zone):
        warn("This method has not been implemented yet.")
        return {}

    def filter_land_areas(self, area):
        warn("This method has not been implemented yet.")
        return {}
    
    def filter_marine_regions(self, region):
        warn("This method has not been implemented yet.")
        return {}