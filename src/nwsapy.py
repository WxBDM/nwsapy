"""These methods are to be called to obtain objects pertaining to the modules.

With how this API is designed, you should be using these functions to access all of the modules (i.e. Alerts,
Radar, Products, etc).

"""
from errors import ParameterTypeError, DataValidationError
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
        An ID corresponding to an alert. If ID is a list, it will iterate through all of the ID's and
        give you an object containing all of the alerts associated with the ID. Note that these alerts may include
        error alerts.

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
    marine_region_string : int, list/tuple
        An ID corresponding to an alert. If ID is a list, it will iterate through all of the ID's and
        give you an object containing all of the alerts associated with the ID. Note that these alerts may include
        error alerts.

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
    """Not implemented."""
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
