
import nwsapy.utils as utils
from collections import OrderedDict
import datetime

# URL constructor flow
#   1. In __init__: Set the data types as such:
#       self.param_dtypes['variable_name'] = ([dtype1, dtype2, ...], Data validation tables)
#       Note that Data Validation Tables should be set to None if there's no data to compare against.
#   2. In __init__: call self._check(params).


class BaseURLConstructor:

    param_dtypes = {}  # this is the dictionary to store all of the parameter types.

    def _check(self, params, valid_dtypes):

        if not any([type(x) in valid_dtypes for x in params.keys()]):
            raise ValueError(f"Value must be one of the following: {', '.join(valid_dtypes)}")

        # Incompatible params: area, point, region, region_type, zone
        keys = params.keys()  # hackish, but save the keys of the input parameters.

        # if there's at least one incompatible type
        if any(x in ['area', 'point', 'region', 'region_type', 'zone'] for x in keys):
            del keys[0]  # delete the first index (guarenteed to be there)
            # if there's another incompatable type, raise a value error.
            if any(x in ['area', 'point', 'region', 'region_type', 'zone'] for x in keys):
                raise ValueError("Incompatible parameters, ensure only one exists: area, point, region, region_type, "
                                 "zone")

        for key, value in self.param_dtypes.items():
            if key in params.keys():
                dtypes = value[0]
                data_validation_table = value[1]

                for user_in_val in params[key]:
                    for data_type in dtypes:
                        if not isinstance(user_in_val, data_type):
                            raise ValueError(f"Data type not same for parameter '{key}'. expected: {data_type}, "
                                             f"got: {type(user_in_val)}. Wrong parameter value: {user_in_val}")

                    if data_validation_table is not None:
                        if user_in_val not in data_validation_table:
                            raise ValueError(f"Data is not in data validation. Value: {user_in_val}.")


class AlertURLConstructor(BaseURLConstructor):

    def all_alert_url_constructor(self, params: dict) -> str:

        for key, value in params.items():
            if not any([isinstance(value, list), isinstance(value, tuple)]):
                params[key] = [value]

        # at a later point, change this to an object oriented approach. It's a lot as it is.
        self.param_dtypes['active'] = ([bool], [True, False])
        self.param_dtypes['area'] = ([str], utils.valid_areas())  # upper cased
        self.param_dtypes['certainty'] = ([str], ["observed", "likely", "possible", "unlikely", "unknown"])
        self.param_dtypes['end'] = ([datetime.datetime], None)
        self.param_dtypes['event'] = ([str], utils.valid_products())
        self.param_dtypes['limit'] = ([int], None)
        self.param_dtypes['message_type'] = ([str], ['alert', 'update', 'cancel'])  # lower case
        self.param_dtypes['point'] = ([float], None)
        self.param_dtypes['region'] = ([str], ['AL', 'AT', 'GM', 'GL', 'PA', 'PI'])  # upper case
        self.param_dtypes['region_type'] = ([str], ['marine', 'land'])  # lower case
        self.param_dtypes['severity'] = ([str], ["extreme", "severe", "moderate", "minor", "unknown"])  # lower case
        self.param_dtypes['start'] = ([datetime.datetime], None)
        self.param_dtypes['status'] = ([str], ["actual", "exercise", "system", "test", "draft"])  # lower case
        self.param_dtypes['urgency'] = ([str], ["immediate", "expected", "future", "past", "unknown"])  # lower case
        self.param_dtypes['zone'] = ([str], None)
        # NOT implemented: cursor, code. I can't even begin to guess what they are.

        # check the data types, ensure they're right.
        self._check(params, [list, bool, str, float, datetime.datetime])

        # ===== FUTURE UPDATE: make it so that capitalization doesn't matter. only have boolean options for now.
        if params['active']: # if it's true
            params['active'] = ['true']
        else:
            params['active'] = ['false']

        # url construction examples:
        #   api.weather.gov/alerts?active=true&status=actual&message_type=alert&area=OK&limit=5
        #   api.weather.gov/alerts?active=true&status=actual&message_type=alert&event=Severe%20Thunderstorm
        #       &region_type=marine&region=GM&area=OK&urgency=past&severity=severe&certainty=possible&limit=5
        #   api.weather.gov/alerts?event=Severe Thunderstorm Warning,Flash Flood Warning

        url = "https://api.weather.gov/alerts"
        url_appends = []
        for key, value in params.items():
            if len(value) == 1:
                url_appends.append(f"{key}={value[0]}")
            else:
                url_appends.append(f"{key}={','.join(value)}")

        url_filter = "&".join(url_appends)
        return "?".join([url, url_filter]).replace(" ", "%20")
