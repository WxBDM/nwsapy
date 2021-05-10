import alerts
import utils


def get_active_alerts():
    """Returns an Alerts object that contains a list and various attributes of the current NWS alerts.

    Returns
    =======
        Alerts => An object containing information about the current alerts.
    """

    response = utils.request("https://api.weather.gov/alerts/active")
    return alerts.ActiveAlerts(response)


def get_alert_by_id(alert_id):
    """Fetches an alert by the ID.

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
            Error: an object containing information about what went wrong.
    """

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

    if not isinstance(marine_region_string, str):
        raise ValueError(f"Parameter must be of type string. Received: {type(marine_region_string)}")

    marine_region_id = marine_region_string.upper()
    if marine_region_id not in ['AL', 'AT', 'GL', 'GM', 'PA', 'PI']:
        raise ValueError(f"Parameter must be either AL, AT, GL, GM, PA, or PI. Value: {marine_region_string}")

    pass


def get_alert_by_area(area_string):
    """temp"""

    if not isinstance(area_string, str):
        raise ValueError(f"Parameter must be of type string. Received: {type(area_string)}")

    area_string = area_string.upper()
    valid_codes = ['AL', 'AK', 'AS', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN',
                   'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
                   'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA',
                   'WA', 'WV', 'WI', 'WY', 'PZ', 'PK', 'PH', 'PS', 'PM', 'AN', 'AM', 'GM', 'LS', 'LM', 'LH', 'LC', 'LE',
                   'LO']

    if area_string not in valid_codes:
        raise ValueError(f"Parameter must be in valid codes. See documentation for valid codes. Value: {area_string}")

    pass
