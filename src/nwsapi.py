import alerts
import utils
from errors import ParameterTypeError, DataValidationError

# General structure:
#   If there's any parameters, perform data validation. Raise a Parameter error if there's an issue with it.
#   Check validation. Is it of proper format (i.e. 2 letters, inside of a list, etc).


def get_active_alerts():
    """Fetches all active alerts.

    Returns
    -------
        Alerts => An object containing information about the current alerts.
    """

    # No parameter data validation checks needed, instantiate object and return it.
    return alerts.ActiveAlerts()


def get_alert_by_id(alert_id):
    """Fetches an alert by the ID.

    Parameters
    ----------
    alert_id : int, list/tuple
        An ID corresponding to an alert. If ID is a list, it will iterate through all of the ID's and
        give you an object containing all of the alerts associated with the ID. Note that these alerts may include
        error alerts.

    Returns
    -------
    alerts.AlertById
    """

    # ensure it's a string.
    if not isinstance(alert_id, str):
        raise ParameterTypeError(alert_id, str)

    return alerts.AlertById(alert_id)


def get_alert_by_marine_region(marine_region_string):
    """Fetches alerts by a marine region.

    Parameters
    ==========
        ID (int, list/tuple): An ID cooresponding to an alert.
            If ID is a list, it will iterate through all of the ID's and give you an object containing all of the alerts
            associated with the ID.

    Returns
    =======
        If successful:
            Alerts: an object containing information about the associated alert(s).
        If unsuccessful:
            Error: an object containing information about what went wrong."""

    # ensure that the parameter is a string.
    if not isinstance(marine_region_string, str):
        raise ParameterTypeError(marine_region_string, str)

    # validate and ensure that it's proper.
    marine_region_id = marine_region_string.upper()
    if marine_region_id not in ['AL', 'AT', 'GL', 'GM', 'PA', 'PI']:
        raise DataValidationError(marine_region_string)


def get_alert_by_area(area):
    """Fetch an alert by an area.

    Parameter
    =========
        area (str): 2 letter area that is one of the valid areas.
        Valid areas:
            'AL', 'AK', 'AS', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA',
            'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
            'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI',
            'WY', 'PZ', 'PK', 'PH', 'PS', 'PM', 'AN', 'AM', 'GM', 'LS', 'LM', 'LH', 'LC', 'LE', 'LO'

    Returns
    =======

    """

    if not isinstance(area, str): # check data type
        raise ParameterTypeError(area, str)

    area = area.upper()
    valid_codes = ['AL', 'AK', 'AS', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN',
                   'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
                   'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA',
                   'WA', 'WV', 'WI', 'WY', 'PZ', 'PK', 'PH', 'PS', 'PM', 'AN', 'AM', 'GM', 'LS', 'LM', 'LH', 'LC', 'LE',
                   'LO']

    if area not in valid_codes:
        raise ValueError(f"Parameter must be in valid codes. See documentation for valid codes. Value: {area}")


def get_total_alert_count():

    # No parameters, create object and return it.
    return alerts.AlertByCount()
