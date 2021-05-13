"""These methods are to be called to obtain objects pertaining to the modules.

With how this API is designed, you should be using these functions to access all of the modules (i.e. Alerts,
Radar, Products, etc).

"""
from typing import Union
import alerts


def get_active_alerts():
    """Fetches all active alerts from ``/alerts/active``

    Returns
    -------
    alerts.ActiveAlerts
        An object that contains the information of the current alerts.
    """

    # No parameter data validation checks needed, instantiate object and return it.
    return alerts.ActiveAlerts()


def get_alert_by_id(alert_id):
    """Fetches an alert by the ID from ``/alerts/{id}``

    Parameters
    ----------
    alert_id : int, list/tuple
        An ID/list of ID's corresponding to an alert.

    Returns
    -------
    alerts.AlertById
        An object containing information of all of the alerts.
    """

    return alerts.AlertById(alert_id)


def get_alert_by_marine_region(marine_region: Union[str, list]):
    """Fetches an alert by the ID from ``/alerts/{id}``

    Parameters
    ----------
    marine_region : int, list/tuple
        A string or list/tuple of strings of the areas to fetch.

    Returns
    -------
    alerts.AlertById
        An object containing information of all of the alerts.

    See Also
    --------
    :ref:`Alerts by Marine Region<alerts_by_marine_table_validation>`
        Table in documentation with valid parameter inputs.

    """
    return alerts.AlertByMarineRegion(marine_region)


def get_alert_by_area(area):
    """Fetches and organizes a count from ``/alerts/active/area/{area}``

    Parameters
    ----------
    area : str, list/tuple
        A string or list/tuple of strings of the areas to fetch.

    Returns
    -------
    alerts.AlertByArea
        An object that contains the information of the alert.

    See Also
    --------
    :ref:`Alerts by Area Table<alerts_by_area_table_validation>`
        Table in documentation with valid parameter inputs.

    """
    return alerts.AlertByArea(area)


def get_alert_count():
    """Fetches and organizes a count from ``/alerts/active/count``

    Returns
    -------
    alerts.AlertByCount
        An object that contains the information of the alert count.

    """
    # No parameters, create object and return it.
    return alerts.AlertByCount()
