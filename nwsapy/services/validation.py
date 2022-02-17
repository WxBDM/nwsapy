"""This contains all of the data validation checking and data used to check
for valid data going into the API. This is generally a step between when the
user interfaces with the entrypoint and before the request is made.

Generally, users _shouldn't_ be accessing the functionality listed in here if
they are using the package as intended. However, if the users wish to utilize
this, then they should import the DataValidationChecker class.
"""

from nwsapy.core.errors import DataValidationError
from nwsapy.core.mapping import full_state_to_two_letter_abbreviation as fsabbr

class DataValidationChecker:
    """Class to encapsulate all data validation checking against API-related
    data inputs.
    
    This class should interface between the programmers and the DataValitationTable
    class, as this class handles the error raising, whereas the DataValidationTable
    class handles if a value is in the DVT or not.
    """
    
    def __init__(self):
        self.dvt = DataValidationTable()
    
    # This class can get cleaned up - there's extra steps the logic is taking,
    # and it would be a good challenge for whoever wants to do it. Primarily,
    # it would focus on eliminating those "extra steps". Right now,
    # params are read in, they're mapped based off of the parameter name,
    # and then the associated function is run, returns either True or False,
    # and if it's false, then it will raise an error.
    
    def check_lat_lon(self, lat, lon):
        """Checks to ensure that the values are within valid lat/lon bounds.

        :param lat: The latitude of the point.
        :type lat: int/float
        :param lon: The longitude of the point.
        :type lon: int/float
        :raises ValueError: Invalid data type for latitude or longitude.
        :raises ValueError: Latitude or longitude is not in valid bounds.
        """
        mapper = {
            'Latitude' : [lat, -90, 90],
            'Longitude' : [lon, -180, 180]
        }
        
        print(type(mapper))
        print(mapper['Latitude'])
        
        for name, data in mapper.items():
            # unpack
            val, min_val, max_val = data
            
            # check dtype
            valid_dtype = any([isinstance(val, int), isinstance(val, float)])
            if not valid_dtype:
                msg = f"{val} is not valid data type. Expected: int/float, Got: {type(val)}"
                raise ValueError(msg)
            
            # check to ensure the values are real coordinates.
            if not min_val <= val <= max_val:
                msg = f'{name} is not between {min_val} and {max_val}. Got: {val}'
                raise ValueError(msg)

    
    def check_active_alerts_dvt(self, params, is_all_alerts = False):
        """Used as the "entrypoint" to checking each parameter against the
        data validation tables.
        
        Used in:
            - ``get_alerts``
            - ``get_active_alerts``

        :param params: Keyword arugments from instantiation of object.
        :type params: dictionary
        :raises DataValidationError:
        """
        url_valid_mapper = {
            'area' : self.dvt.is_valid_area,
            'certainty' : self.dvt.is_valid_certainty,
            'event' : self.dvt.is_valid_product,
            'message_type' : self.dvt.is_valid_message_type,
            'region' : self.dvt.is_valid_region,
            'region_type' : self.dvt.is_valid_region_type,
            'severity' : self.dvt.is_valid_severity,
            'status' : self.dvt.is_valid_status,
            'urgency' : self.dvt.is_valid_urgency
        }
        
        if is_all_alerts:
            url_valid_mapper['limit'] = self.is_above_limit
        
        # iterate through the parameters and check to ensure that the
        # values are values.
        for key, value in params.items():
            if key not in url_valid_mapper:
                continue # TODO: look into other ways to handle this.
            
            # equivalent to: is_valid = self.is_valid_xyz(value)
            
            # Sometimes, it'll be read in as a list. Other times, it won't.
            # So, convert it into a list if it's not and then iterate through
            # it :)
            if not any([isinstance(value, list), isinstance(value, tuple)]):
                value = [value]
            
            for val in value:    
                is_valid = url_valid_mapper[key](val)
            
                if not is_valid:
                    raise DataValidationError(value, f"Parameter: `{key}`")

    def check_if_valid_area(self, area):
        """Checks to see if it's a valid area.
        
        Used in:
            - ``get_alert_by_area``
        """
        if not self.dvt.is_valid_area(area):
            raise DataValidationError(area, f"Area: `{area}")
    
    def check_if_valid_marine_region(self, marine_region):
        if not self.dvt.is_valid_region(marine_region):
            raise DataValidationError(marine_region, f'Region: `{marine_region}`')


class DataValidationTable:

    @staticmethod
    def is_above_limit(limit):
        
        if isinstance(limit, float):
            limit = int(limit)
        if not isinstance(limit, int):
            raise TypeError(f'Limit not integer or float. Found: {type(limit)}')
        
        if limit > 500:
            return True
        return False

    @staticmethod
    def is_valid_area(area):
        """Checks against all valid areas that the API offers.
        
        See the Data Validation Table section of the documentation for
        a full and complete list of valid entries.

        :param area: The 2 state abbreviation or full name of state.
        :type area: str
        :return: True if it's a valid area, false otherwise
        :rtype: bool
        """
        # Note that fsabbr handles .title() functionality.
        if len(area) != 2: # is not a 2 letter abbreviation, make it a 2 letter.
            area = fsabbr(area)
        
        if area in valid_areas():
            return True
        
        return False
    
    @staticmethod
    def is_valid_product(product):
        """Checks to ensure that the product is a valid product.
        
        .. note::
            The capitalization and spelling _must_ be the same. Under the hood,
            it's a string comparison, and it doesn't take into account spelling
            errors.
            
        See the Data Validation Table section of the documentation for
        a full and complete list of valid entries.
        
        :param product: The desired NWS product.
        :type product: str
        :return: True if it's valid, False otherwise.
        :rtype: bool
        """
        if product in valid_products():
            return True
        
        return False

    @staticmethod
    def is_valid_certainty(certainty):
        """Checks to ensure that the ceratinty is a valid certainty.

        See the Data Validation Table section of the documentation for
        a full and complete list of valid entries.

        :param certainty: The certainty level to check.
        :type certainty: str
        :return: True if it's valid, False otherwise.
        :rtype: bool
        """
        if certainty in valid_certainties():
            return True
        
        return False
    
    @staticmethod
    def is_valid_message_type(message_type):
        """Checks to ensure that the message type is a valid message type.

        See the Data Validation Table section of the documentation for
        a full and complete list of valid entries.

        :param certainty: The certainty level to check.
        :type certainty: str
        :return: True if it's valid, False otherwise.
        :rtype: bool
        """
        if message_type in valid_message_types():
            return True
        
        return False

    @staticmethod
    def is_valid_region(region):
        # TODO: Add in docstring similar to above.
        if region in valid_regions():
            return True
        return False
    
    @staticmethod
    def is_valid_region_type(region_type):
        # TODO: Add in docstring similar to above.
        if region_type in valid_region_types():
            return True
        return False
    
    @staticmethod 
    def is_valid_severity(severity):
        # TODO: Add in docstring similar to above.
        if severity in valid_severity():
            return True
        return False
    
    @staticmethod
    def is_valid_status(status):
        # TODO: Add in docstring similar to above.
        if status in valid_status():
            return True
        return False
    
    @staticmethod
    def is_valid_urgency(urgency):
        # TODO: Add in docstring similar to above.
        if urgency in valid_urgency():
            return True
        return False

# these functions aren't built into the above class for a few reasons:
#   1. Maybe the users want to breach outside of the entrypoint and use
#       these for whatever reason.
#   2. It doesn't make sense to instantiate new objects with these
#       every time NWSAPy constructs a URL.

def valid_certainties():
    """Returns a list of valid certainties

    :return: A list of valid certainties, all lowercase.
    :rtype: list[str]
    """
    return ['Observed', 'Likely', 'Possible', 'Unlikely', 'Unknown']

def valid_message_types():
    """Returns a list of valid message types.

    :return: A list of valid message types, all lowercase.
    :rtype: list[str]
    """
    # NWS API requires this to be lowercase
    return ['alert', 'update', 'cancel']

def valid_regions():
    """Returns a list of valid 2 letter uppercase regions.

    :return: A list of 2 letter uppercase regions.
    :rtype: list
    """
    return ['AL', 'AT', 'GM', 'GL', 'PA', 'PI']

def valid_region_types():
    """Returns a list of valid region types (land or marine), all lowercase.

    :return: A list of valid region types.
    :rtype: list[str]
    """
    return ['Marine', 'Land']

def valid_severity():
    """Returns a list of valid severity levels, all lowercase.

    :return: A list of valid severity levels.
    :rtype: list[str]
    """
    return ["Extreme", "Severe", "Moderate", "Minor", "Unknown"]

def valid_status():
    """Returns a list of valid status levels, all lowercase.

    :return: A list of status levels.
    :rtype: list[str]
    """
    return ["Actual", "Exercise", "System", "Test", "Draft"]

def valid_urgency():
    """Returns a list of valid urgency levels, all lowercase.

    :return: A list of valid urgency levels.
    :rtype: list[str]
    """
    return ["Immediate", "Expected", "Future", "Past", "Unknown"]

def valid_areas():
    """Returns a list of valid 2 letter state abbreviations.

    :return: A list of valid areas, all upper case 2 letter abbreviations.
    :rtype: list[str]
    """
    return ['AL', 'AK', 'AS', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 
            'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 
            'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY',
            'PZ', 'PK', 'PH', 'PS', 'PM', 'AN', 'AM', 'GM', 'LS', 'LM', 'LH',
            'LC', 'LE', 'LO'
            ]

def valid_products():
    """Returns a list of all valid NWS products.
    
    .. note::
        If checking for a valid product,

    :return: A list of valid NWS products.
    :rtype: list[str]
    """
    return ['911 Telephone Outage Emergency', 'Administrative Message',
            'Air Quality Alert', 'Air Stagnation Advisory',
            'Arroyo And Small Stream Flood Advisory', 'Ashfall Advisory',
            'Ashfall Warning', 'Avalanche Advisory', 'Avalanche Warning',
            'Avalanche Watch', 'Beach Hazards Statement', 'Blizzard Warning',
            'Blizzard Watch', 'Blowing Dust Advisory', 'Blowing Dust Warning',
            'Brisk Wind Advisory', 'Child Abduction Emergency',
            'Civil Danger Warning', 'Civil Emergency Message', 
            'Coastal Flood Advisory', 'Coastal Flood Statement',
            'Coastal Flood Warning', 'Coastal Flood Watch', 'Dense Fog Advisory',
            'Dense Smoke Advisory', 'Dust Advisory', 'Dust Storm Warning',
            'Earthquake Warning', 'Evacuation - Immediate', 'Excessive Heat Warning',
            'Excessive Heat Watch', 'Extreme Cold Warning', 'Extreme Cold Watch',
            'Extreme Fire Danger', 'Extreme Wind Warning', 'Fire Warning',
            'Fire Weather Watch', 'Flash Flood Statement', 'Flash Flood Warning',
            'Flash Flood Watch', 'Flood Advisory', 'Flood Statement',
            'Flood Warning', 'Flood Watch', 'Freeze Warning', 'Freeze Watch',
            'Freezing Fog Advisory', 'Freezing Rain Advisory',
            'Freezing Spray Advisory', 'Frost Advisory', 'Gale Warning',
            'Gale Watch', 'Hard Freeze Warning', 'Hard Freeze Watch', 
            'Hazardous Materials Warning', 'Hazardous Seas Warning',
            'Hazardous Seas Watch', 'Hazardous Weather Outlook', 'Heat Advisory',
            'Heavy Freezing Spray Warning', 'Heavy Freezing Spray Watch',
            'High Surf Advisory', 'High Surf Warning', 'High Wind Warning',
            'High Wind Watch', 'Hurricane Force Wind Warning',
            'Hurricane Force Wind Watch', 'Hurricane Local Statement',
            'Hurricane Warning', 'Hurricane Watch', 'Hydrologic Advisory',
            'Hydrologic Outlook', 'Ice Storm Warning', 'Lake Effect Snow Advisory',
            'Lake Effect Snow Warning', 'Lake Effect Snow Watch',
            'Lake Wind Advisory', 'Lakeshore Flood Advisory',
            'Lakeshore Flood Statement', 'Lakeshore Flood Warning',
            'Lakeshore Flood Watch', 'Law Enforcement Warning',
            'Local Area Emergency', 'Low Water Advisory',
            'Marine Weather Statement', 'Nuclear Power Plant Warning',
            'Radiological Hazard Warning', 'Red Flag Warning',
            'Rip Current Statement', 'Severe Thunderstorm Warning',
            'Severe Thunderstorm Watch', 'Severe Weather Statement',
            'Shelter In Place Warning', 'Short Term Forecast',
            'Small Craft Advisory', 'Small Craft Advisory For Hazardous Seas',
            'Small Craft Advisory For Rough Bar', 'Small Craft Advisory For Winds',
            'Small Stream Flood Advisory', 'Snow Squall Warning', 'Special Marine Warning',
            'Special Weather Statement', 'Storm Surge Warning', 'Storm Surge Watch',
            'Storm Warning', 'Storm Watch', 'Test', 'Tornado Warning', 'Tornado Watch',
            'Tropical Depression Local Statement', 'Tropical Storm Local Statement',
            'Tropical Storm Warning', 'Tropical Storm Watch', 'Tsunami Advisory',
            'Tsunami Warning', 'Tsunami Watch', 'Typhoon Local Statement',
            'Typhoon Warning', 'Typhoon Watch',
            'Urban And Small Stream Flood Advisory', 'Volcano Warning',
            'Wind Advisory', 'Wind Chill Advisory', 'Wind Chill Warning',
            'Wind Chill Watch', 'Winter Storm Warning', 'Winter Storm Watch', 
            'Winter Weather Advisory'
            ]
