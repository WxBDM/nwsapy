"""These methods are to be called to obtain objects pertaining to the modules.

With how this API is designed, you should be using these functions to access all of the modules (i.e. Alerts,
Radar, Products, etc).

"""
from typing import Union
import alerts
import utils
import dbcomms
from errors import ParameterTypeError

# needed: https://api.weather.gov/openapi.json


def set_user_agent(my_app, contact):
    """Sets the User-Agent in header for requests. This should be unique to your application.

    The User-Agent header format is as such: (my_app, contact) where my_app is your application name and contact
    is an email address you can be contacted at in the event that the maintainers of the NWS API needed
    to contact you.

    """

    # check data types
    if not isinstance(my_app, str):
        raise ParameterTypeError(my_app, str)
    if not isinstance(contact, str):
        raise ParameterTypeError(contact, str)

    user_agent_str = f'({my_app}, {contact})'
    dbcomms.set_user_agent(user_agent_str)


def get_all_alerts() -> alerts.AllAlerts:
    """Fetches all active alerts from ``/alerts``.

    Returns
    -------
    :class:`alerts.AllAlerts`
        An object that contains the information of all alerts.
    """
    return alerts.AllAlerts()


def get_active_alerts() -> alerts.ActiveAlerts:
    """Fetches all active alerts from ``/alerts/active``.

    Returns
    -------
    alerts.ActiveAlerts
        An object that contains the information of the current alerts.
    """

    # No parameter data validation checks needed, instantiate object and return it.
    return alerts.ActiveAlerts()


def get_alert_types() -> alerts.AlertTypes:
    """Fetches the alert types from ``/alerts/types``.

    Returns
    -------
    :class:`alerts.Types`
        An object containing information of the alert types.
    """

    return alerts.AlertTypes()


def get_alert_by_id(alert_id: Union[str, list]) -> alerts.AlertById:
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

    return alerts.AlertById(alert_id)


def get_alert_by_marine_region(marine_region: Union[str, list]) -> alerts.AlertByMarineRegion:
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
    return alerts.AlertByMarineRegion(marine_region)


def get_alert_by_area(area: Union[str, list]) -> alerts.AlertByArea:
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
    return alerts.AlertByArea(area)


def get_alert_count() -> alerts.AlertByCount:
    """Fetches and organizes a count from ``/alerts/active/count``.

    Returns
    -------
    :class:`alerts.AlertByCount`
        An object that contains the information of the alert count.

    """
    # No parameters, create object and return it.
    return alerts.AlertByCount()


def ping_server() -> utils.ServerPing:
    """Pings https://api.weather.gov/ to see status

    Returns
    -------
    :class:`utils.ServerPing`
    """

    return utils.ServerPing()
