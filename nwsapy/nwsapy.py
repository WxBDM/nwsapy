"""These methods are to be called to obtain objects pertaining to the modules.

With how this API is designed, you should be using these functions to access all of the modules (i.e. Alerts,
Radar, Products, etc).

"""
import datetime
from typing import Union
from collections import OrderedDict

import nwsapy.utils as utils
import nwsapy.alerts as alerts
import nwsapy.points as points
import nwsapy.glossary as glossary  # don't put anyting after this, IDE gives weird error.
from nwsapy.errors import ParameterTypeError


# needed: https://api.weather.gov/openapi.json


class NWSAPy:
    _app = None
    _contact = None
    _user_agent = "(no app name set, no email set)"
    _user_agent_to_d = {'User-Agent': _user_agent}

    def _check_user_agent(self):
        if self._user_agent == "(no app name set, no email set)":
            print(f"Be sure to set the user agent before calling any nwsapy functions. To prevent this message from "
                  f"appearing again, use: nwsapy.set_user_agent(app_name, email)")

    def set_user_agent(self, app_name, contact):
        """Sets the User-Agent in header for requests. This should be unique to your application.

        From the NWS API documentation: "A User Agent is required to identify your application.
        This string can be anything, and the more unique to your application the less likely it will be
        affected by a security event. If you include contact information (website or email), we can contact
        you if your string is associated to a security event."
        (Link: https://www.weather.gov/documentation/services-web-api#/)

        Parameters
        ----------
        app_name : str
            The name of your application.
        contact : str
            The contact email. This is needed for API authentication.

        """

        # check data types
        if not isinstance(app_name, str):
            raise ParameterTypeError(app_name, str)
        if not isinstance(contact, str):
            raise ParameterTypeError(contact, str)

        self._app = app_name
        self._contact = contact
        self._user_agent = f"({self._app}, {contact})"
        self._user_agent_to_d = dict({'User-Agent': self._user_agent})

    def get_all_alerts(self, active: bool = None, area: list or str = None, certainty: list or str = None,
                       end: datetime.datetime = None, event: list or str = None, limit: int = None,
                       message_type: list or str = None, point: list = None, region: list or str = None,
                       region_type: str = None, severity: list or str = None, start: datetime.datetime = None,
                       status: list or str = None, urgency: list or str = None, zone: list or str = None
                       ) -> alerts.AllAlerts:
        """Fetches all active alerts from ``/alerts``.

        IMPORTANT: You must ensure capitalization is correct for area, event, message_type, region, region_type,
            severity, status, urgency, and zone. See documentation for valid parameters.

        Parameters
        ----------
        active: bool
            If the alert is active or not.

        area: str or list[str]
            The area in which the alert is in. Valid parameters are typically the 2 letter abbreviation of the state
            in upper case (i.e. "AL", "PA", etc)

        certainty: str or list[str]
            The certainty of the alert. Valid parameters: "observed", "likely", "possible", "unlikely", "unknown"

        end: datetime.datetime (local time)
            The ending time for all alerts. All alerts up to the ending time are included.

        event: str or list[str]
            The type of alert (i.e. Severe Thunderstorm Warning, etc). Valid parameters are found on the data validation
                table.

        limit: int
            The number of alerts to return at most. Will only retrieve the first n alerts.

        message_type: str or list[str]
            Either alert

        Returns
        -------
        :class:`alerts.AllAlerts`
            An object that contains the information of all alerts.
        """
        self._check_user_agent()  # if user agent isn't set, print it
        param_d = {'active': active, 'area': area, 'certainty': certainty, 'end': end, 'event': event,
                   'limit': limit, 'message_type': message_type, 'point': point, 'region': region,
                   'region_type': region_type, 'severity': severity, 'start': start, 'status': status,
                   'urgency': urgency, 'zone': zone}

        utils.eliminate_none_in_param_d(param_d)  # gets rid of the "None"s from the parameters.
        return alerts.AllAlerts(self._user_agent_to_d, param_d)

    def get_active_alerts(self) -> alerts.ActiveAlerts:
        """Fetches all active alerts from ``/alerts/active``.

        Returns
        -------
        alerts.ActiveAlerts
            An object that contains the information of the current alerts.
        """
        self._check_user_agent()
        return alerts.ActiveAlerts(self._user_agent_to_d)

    def get_alert_types(self) -> alerts.AlertTypes:
        """Fetches the alert types from ``/alerts/types``.

        Returns
        -------
        :class:`alerts.AlertTypes`
            An object containing information of the alert types.
        """
        self._check_user_agent()
        return alerts.AlertTypes(self._user_agent_to_d)

    def get_alert_by_id(self, alert_id: Union[str, list]) -> alerts.AlertById:
        """Fetches an alert by the ID from ``/alerts/{id}``.

        Parameters
        ----------
        alert_id : int, list/tuple
            An ID/list of ID's corresponding to an alert.

        Returns
        -------
        :class:`alerts.AlertById`
            An object containing information of all of the alerts.
        """
        self._check_user_agent()
        return alerts.AlertById(alert_id, self._user_agent_to_d)

    def get_alert_by_marine_region(self, marine_region: Union[str, list]) -> alerts.AlertByMarineRegion:
        """Fetches an alert by the ID from ``/alerts/{id}``.

        Parameters
        ----------
        marine_region : int, list/tuple
            A string or list/tuple of strings of the areas to fetch.

        Returns
        -------
        :class:`alerts.AlertById`
            An object containing information of all of the alerts.

        See Also
        --------
        :ref:`Alerts by Marine Region<alerts_by_marine_table_validation>`
            Table in documentation with valid parameter inputs.

        """
        self._check_user_agent()
        return alerts.AlertByMarineRegion(marine_region, self._user_agent_to_d)

    def get_alert_by_area(self, area: Union[str, list]) -> alerts.AlertByArea:
        """Fetches and organizes a count from ``/alerts/active/area/{area}``.

        Parameters
        ----------
        area : str, list/tuple
            A string or list/tuple of strings of the areas to fetch.

        Returns
        -------
        :class:`alerts.AlertByArea`
            An object that contains the information of the alert.

        See Also
        --------
        :ref:`Alerts by Area Table<alerts_by_area_table_validation>`
            Table in documentation with valid parameter inputs.

        """
        self._check_user_agent()
        return alerts.AlertByArea(area, self._user_agent_to_d)

    def get_alert_count(self) -> alerts.AlertByCount:
        """Fetches and organizes a count from ``/alerts/active/count``.

        Returns
        -------
        :class:`alerts.AlertByCount`
            An object that contains the information of the alert count.

        """
        self._check_user_agent()
        return alerts.AlertByCount(self._user_agent_to_d)

    def ping_server(self) -> alerts.ServerPing:
        """Pings https://api.weather.gov/ to see status

        Returns
        -------
        :class:`utils.ServerPing`
        """
        self._check_user_agent()
        return alerts.ServerPing(self._user_agent_to_d)

    def get_alert_by_zone(self, zone_id: Union[str, list]) -> alerts.AlertByZone:
        """Fetches an alert by the zone ID from ``/alerts/zone/{zoneId}``.

        Parameters
        ----------
        zone_id : int, list/tuple
            An ID/list of ID's corresponding to an alert.

        Returns
        -------
        :class:`alerts.AlertByZone`
            An object containing information of all of the alerts.
        """
        self._check_user_agent()
        return alerts.AlertByZone(zone_id, self._user_agent_to_d)

    def get_glossary(self):
        """Returns the AMS glossary.

        Returns
        -------
        :class:`glossary.Glossary`
            An object containing the entire AMS glossary.
        """
        self._check_user_agent()
        return glossary.Glossary(self._user_agent_to_d)

    def get_point(self, lat, lon):
        """Gets a point from the API."""

        self._check_user_agent()
        return points.Point(lat, lon, self._user_agent_to_d)

    def get_point_station(self, lat, lon):
        """Retrieves a point's station information.

        Returns
        -------
        :class:`points.PointStation`
            An object containing information from /points/stations
        """

        self._check_user_agent()
        return points.PointStation(lat, lon, self._user_agent_to_d)
