"""These methods are to be called to obtain objects pertaining to the modules.

With how this API is designed, you should be using these functions to access all of the modules (i.e. Alerts,
Radar, Products, etc).

"""
from typing import Union
import nwsapy.alerts as alerts
from nwsapy.errors import ParameterTypeError

# needed: https://api.weather.gov/openapi.json


class nwsapy:

    _app = None
    _contact = None
    _user_agent = "(NWSAPy, test@test.com)"
    _user_agent_to_d = {'User-Agent' : _user_agent}

    def _check_user_agent(self):
        if self._user_agent == "(NWSAPy, test@test.com)":
            print("Be sure to set the user agent. To prevent this message from appearing"
                  " again, use: nwsapy.set_user_agent(app_name, contact)")

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
        self._user_agent_to_d = dict({'User-Agent' : self._user_agent})

    def get_all_alerts(self) -> alerts.AllAlerts:
        """Fetches all active alerts from ``/alerts``.

        Returns
        -------
        :class:`alerts.AllAlerts`
            An object that contains the information of all alerts.
        """
        self._check_user_agent()
        return alerts.AllAlerts(self._user_agent_to_d)

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

