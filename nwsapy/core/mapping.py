"""This file is intended to be a mapping to some of the more common
meteorological/geography things. There are some functions
that are used for other parts of NWSAPy."""

from .errors import DataValidationError

def state_abbreviation_to_full_name(abbr):
    """Converts a 2 letter state abbreviation to the respective full name.

    Example: 'ND' will return 'North Dakota'

    :param abbr: The 2 letter abbreviation for a state.
    :returns: Full name corresponding to the parameter.
    """
    abbr_upper = abbr.upper() # transform it to uppercase
    if abbr not in abbr_state:
        e_msg = f'{abbr} not found in 2 letter abbreviation of states.'
        raise DataValidationError(e_msg)

    return abbr_state[abbr_upper]


def full_state_to_two_letter_abbreviation(full_state_name):
    """Converts a full state name to the respective 2 letter abbreviation.

    Example: 'New York' will return 'NY'

    :param full_state_name: The full name of the state.
    :returns: 2 letter abbreviation of the full state name.
    """
    full_title = full_state_name.title()
    if full_title not in full_state:
        e_msg = f'{full_state_name} not found in state names. Ensure spelling '\
            'is correct.'
        raise DataValidationError(e_msg)

    return full_state[full_title]


def get_hex_for_alert(alert):
    """Returns a hex value for a given alert

    :param alert: The alert to get the associated hex value for.
    :type alert: string
    """
    
    # title it, keep it consistent.
    alert_fixed = alert.title()
    # validation check
    if alert_fixed not in colors:
        e_msg = f'{alert} not a valid alert. Check spelling. See documentation '\
            'for valid alerts.'
        raise DataValidationError(e_msg)

    # all good, return it.
    return f"#{colors[alert_fixed]['hex']}"


def get_rgb_for_alert(alert):
    """Returns a RGB pairing for a given alert

    :param alert: The alert to get the associated RGB for.
    :type alert: string
    """
     # title it, keep it consistent.
    alert_fixed = alert.title()
    # validation check
    if alert_fixed not in colors:
        e_msg = f'{alert} not a valid alert. Check spelling. See documentation '\
            'for valid alerts.'
        raise DataValidationError(e_msg)

    # all good, return it.
    return colors[alert]['rgb']

abbr_state = {'AL' : 'Alabama', 'AK' : 'Alaska', 'AR' : 'Arkansas', 'AZ' : 'Arizona',
              'CA' : 'California', 'CO' : 'Colorado', 'CT' : 'Connecticut',
              'DE' : 'Deleware', 'DC' : 'Washington D.C.', 'FL' : 'Florida',
              'GA' : 'Georiga', 'GU' : 'Guam', 'HI' : 'Hawaii', 'ID' : 'Idaho',
              'IL' : 'Illinois', 'IN' : 'Indiana', 'IA' : 'Iowa', 'KS' : 'Kansas',
              'KY' : 'Kentucky', 'LA' : 'Louisiana', 'ME' : 'Maine', 'MD' : 'Maryland',
              'MA' : 'Massachusetts', 'MI' : 'Michigan', 'MN' : 'Minnesota',
              'MS' : 'Mississippi', 'MO' : 'Montana', 'NE' : 'Nebraska',
              'NV' : 'Nevada', 'NH' : 'New Hampshire', 'NJ' : 'New Jersey',
              'NM' : 'New Mexico', 'NY' : 'New York', 'NC' : 'North Carolina',
              'ND' : 'North Dakota', 'OH' : 'Ohio', 'OK' : 'Oklahoma', 'OR' : 'Oregon',
              'PA' : 'Pennyslvania', 'PR' : 'Puerto Rico', 'RI' : 'Rhode Island',
              'SC' : 'South Carolina', 'SD' : 'South Dakota', 'TN' : 'Tennessee',
              'TX' : 'Texas', 'UT' : 'Utah', 'VT' : 'Vermont', 'VI' : 'Virgin Islands',
              'VA' : 'Virginia', 'WA' : 'Washington', 'WV' : 'West Virginia',
              'WI' : 'Wisconsin', 'WY' : 'Wyoming'
              }

# If iterating through a full list of state names, instead of taking the above
# dictionary and flipping it, it would be quicker to run if hardcoded.
full_state = {'Alabama': 'AL', 'Alaska': 'AK', 'Arkansas': 'AR', 'Arizona': 'AZ',
              'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
              'Deleware': 'DE', 'Washington D.C.': 'DC', 'Florida': 'FL',
              'Georiga': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID',
              'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
              'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
              'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
              'Mississippi': 'MS', 'Montana': 'MO', 'Nebraska': 'NE',
              'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
              'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
              'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
              'Pennyslvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI',
              'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
              'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI',
              'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
              'Wisconsin': 'WI', 'Wyoming': 'WY'
              }

# Mapping for colors of NWS alerts.
colors = {'911 Telephone Outage': {'hex': 'C0C0C0', 'rgb': '192 192 192'},
          'Administrative Message': {'hex': 'C0C0C0', 'rgb': '192 192 192'},
          'Air Quality Alert': {'hex': '808080', 'rgb': '128 128 128'},
          'Air Stagnation Advisory': {'hex': '808080', 'rgb': '128 128 128'},
          'Arroyo and Small Stream Flood Advisory': {'hex': '00FF7F',
                                                     'rgb': '0 255 127'},
          'Ashfall Advisory': {'hex': '696969', 'rgb': '105 105 105'},
          'Ashfall Warning': {'hex': 'A9A9A9', 'rgb': '169 169 169'},
          'Avalanche Advisory': {'hex': 'CD853F', 'rgb': '205 133 63'},
          'Avalanche Warning': {'hex': '1E90FF', 'rgb': '30 144 255'},
          'Avalanche Watch': {'hex': 'F4A460', 'rgb': '244 164 96'},
          'Beach Hazards Statement': {'hex': '40E0D0', 'rgb': '64 224 208'},
          'Blizzard Warning': {'hex': 'FF4500', 'rgb': '255 69 0'},
          'Blizzard Watch': {'hex': 'ADFF2F', 'rgb': '173 255 47'},
          'Blowing Dust Advisory': {'hex': 'BDB76B', 'rgb': '189 183 107'},
          'Blowing Dust Warning': {'hex': 'FFE4C4', 'rgb': '255 228 196'},
          'Blue Alert': {'hex': 'FFFFFF', 'rgb': '255 255 255'},
          'Brisk Wind Advisory': {'hex': 'D8BFD8', 'rgb': '216 191 216'},
          'Child Abduction Emergency': {'hex': 'FFFFFF', 'rgb': '255 255 255'},
          'Civil Danger Warning': {'hex': 'FFB6C1', 'rgb': '255 182 193'},
          'Civil Emergency Message': {'hex': 'FFB6C1', 'rgb': '255 182 193'},
          'Coastal Flood Advisory': {'hex': '7CFC00', 'rgb': '124 252 0'},
          'Coastal Flood Statement': {'hex': '6B8E23', 'rgb': '107 142 35'},
          'Coastal Flood Warning': {'hex': '228B22', 'rgb': '34 139 34'},
          'Coastal Flood Watch': {'hex': '66CDAA', 'rgb': '102 205 170'},
          'Dense Fog Advisory': {'hex': '708090', 'rgb': '112 128 144'},
          'Dense Smoke Advisory': {'hex': 'F0E68C', 'rgb': '240 230 140'},
          'Dust Advisory': {'hex': 'BDB76B', 'rgb': '189 183 107'},
          'Dust Storm Warning': {'hex': 'FFE4C4', 'rgb': '255 228 196'},
          'Earthquake Warning': {'hex': '8B4513', 'rgb': '139 69 19'},
          'Evacuation Immediate': {'hex': '7FFF00', 'rgb': '127 255 0'},
          'Excessive Heat Warning': {'hex': 'C71585', 'rgb': '199 21 133'},
          'Excessive Heat Watch': {'hex': '800000', 'rgb': '128 0 0'},
          'Extreme Cold Warning': {'hex': '0000FF', 'rgb': '0 0 255'},
          'Extreme Cold Watch': {'hex': '0000FF', 'rgb': '0 0 255'},
          'Extreme Fire Danger': {'hex': 'E9967A', 'rgb': '233 150 122'},
          'Extreme Wind Warning': {'hex': 'FF8C00', 'rgb': '255 140 0'},
          'Fire Warning': {'hex': 'A0522D', 'rgb': '160 82 45'},
          'Fire Weather Watch': {'hex': 'FFDEAD', 'rgb': '255 222 173'},
          'Flash Flood Statement': {'hex': '8B0000', 'rgb': '139 0 0'},
          'Flash Flood Warning': {'hex': '8B0000', 'rgb': '139 0 0'},
          'Flash Flood Watch': {'hex': '2E8B57', 'rgb': '46 139 87'},
          'Flood Advisory': {'hex': '00FF7F', 'rgb': '0 255 127'},
          'Flood Statement': {'hex': '00FF00', 'rgb': '0 255 0'},
          'Flood Warning': {'hex': '00FF00', 'rgb': '0 255 0'},
          'Flood Watch': {'hex': '2E8B57', 'rgb': '46 139 87'},
          'Freeze Warning': {'hex': '483D8B', 'rgb': '72 61 139'},
          'Freeze Watch': {'hex': '00FFFF', 'rgb': '0 255 255'},
          'Freezing Fog Advisory': {'hex': '008080', 'rgb': '0 128 128'},
          'Freezing Spray Advisory': {'hex': '00BFFF', 'rgb': '0 191 255'},
          'Frost Advisory': {'hex': '6495ED', 'rgb': '100 149 237'},
          'Gale Warning': {'hex': 'DDA0DD', 'rgb': '221 160 221'},
          'Gale Watch': {'hex': 'FFC0CB', 'rgb': '255 192 203'},
          'Hard Freeze Warning': {'hex': '9400D3', 'rgb': '148 0 211'},
          'Hard Freeze Watch': {'hex': '4169E1', 'rgb': '65 105 225'},
          'Hazardous Materials Warning': {'hex': '4B0082', 'rgb': '75 0 130'},
          'Hazardous Seas Warning': {'hex': 'D8BFD8', 'rgb': '216 191 216'},
          'Hazardous Seas Watch': {'hex': '483D8B', 'rgb': '72 61 139'},
          'Hazardous Weather Outlook': {'hex': 'EEE8AA', 'rgb': '238 232 170'},
          'Heat Advisory': {'hex': 'FF7F50', 'rgb': '255 127 80'},
          'Heavy Freezing Spray Warning': {'hex': '00BFFF', 'rgb': '0 191 255'},
          'Heavy Freezing Spray Watch': {'hex': 'BC8F8F', 'rgb': '188 143 143'},
          'High Surf Advisory': {'hex': 'BA55D3', 'rgb': '186 85 211'},
          'High Surf Warning': {'hex': '228B22', 'rgb': '34 139 34'},
          'High Wind Warning': {'hex': 'DAA520', 'rgb': '218 165 32'},
          'High Wind Watch': {'hex': 'B8860B', 'rgb': '184 134 11'},
          'Hurricane Force Wind Warning': {'hex': 'CD5C5C', 'rgb': '205 92 92'},
          'Hurricane Force Wind Watch': {'hex': '9932CC', 'rgb': '153 50 204'},
          'Hurricane Local Statement': {'hex': 'FFE4B5', 'rgb': '255 228 181'},
          'Hurricane Warning': {'hex': 'DC143C', 'rgb': '220 20 60'},
          'Hurricane Watch': {'hex': 'FF00FF', 'rgb': '255 0 255'},
          'Hydrologic Advisory': {'hex': '00FF7F', 'rgb': '0 255 127'},
          'Hydrologic Outlook': {'hex': '90EE90', 'rgb': '144 238 144'},
          'Ice Storm Warning': {'hex': '8B008B', 'rgb': '139 0 139'},
          'Lake Effect Snow Warning': {'hex': '008B8B', 'rgb': '0 139 139'},
          'Lake Effect Snow Watch': {'hex': '87CEFA', 'rgb': '135 206 250'},
          'Lake Wind Advisory': {'hex': 'D2B48C', 'rgb': '210 180 140'},
          'Lakeshore Flood Advisory': {'hex': '7CFC00', 'rgb': '124 252 0'},
          'Lakeshore Flood Statement': {'hex': '6B8E23', 'rgb': '107 142 35'},
          'Lakeshore Flood Warning': {'hex': '228B22', 'rgb': '34 139 34'},
          'Lakeshore Flood Watch': {'hex': '66CDAA', 'rgb': '102 205 170'},
          'Law Enforcement Warning': {'hex': 'C0C0C0', 'rgb': '192 192 192'},
          'Local Area Emergency': {'hex': 'C0C0C0', 'rgb': '192 192 192'},
          'Low Water Advisory': {'hex': 'A52A2A', 'rgb': '165 42 42'},
          'Marine Weather Statement': {'hex': 'FFDAB9', 'rgb': '255 239 213'},
          'Nuclear Power Plant Warning': {'hex': '4B0082', 'rgb': '75 0 130'},
          'Radiological Hazard Warning': {'hex': '4B0082', 'rgb': '75 0 130'},
          'Red Flag Warning': {'hex': 'FF1493', 'rgb': '255 20 147'},
          'Rip Current Statement': {'hex': '40E0D0', 'rgb': '64 224 208'},
          'Severe Thunderstorm Warning': {'hex': 'FFA500', 'rgb': '255 165 0'},
          'Severe Thunderstorm Watch': {'hex': 'DB7093', 'rgb': '219 112 147'},
          'Severe Weather Statement': {'hex': '00FFFF', 'rgb': '0 255 255'},
          'Shelter In Place Warning': {'hex': 'FA8072', 'rgb': '250 128 114'},
          'Short Term Forecast': {'hex': '98FB98', 'rgb': '152 251 152'},
          'Small Craft Advisory': {'hex': 'D8BFD8', 'rgb': '216 191 216'},
          'Small Craft Advisory For Hazardous Seas': {'hex': 'D8BFD8',
                                                      'rgb': '216 191 216'},
          'Small Craft Advisory for Rough Bar': {'hex': 'D8BFD8',
                                                 'rgb': '216 191 216'},
          'Small Craft Advisory for Winds': {'hex': 'D8BFD8',
                                             'rgb': '216 191 216'},
          'Small Stream Flood Advisory': {'hex': '00FF7F', 'rgb': '0 255 127'},
          'Snow Squall Warning': {'hex': 'C71585', 'rgb': '199 21 133'},
          'Special Marine Warning': {'hex': 'FFA500', 'rgb': '255 165 0'},
          'Special Weather Statement': {'hex': 'FFE4B5', 'rgb': '255 228 181'},
          'Storm Surge Warning': {'hex': 'B524F7', 'rgb': '181 36 247'},
          'Storm Surge Watch': {'hex': 'DB7FF7', 'rgb': '219 127 247'},
          'Storm Warning': {'hex': '9400D3', 'rgb': '148 0 211'},
          'Storm Watch': {'hex': 'FFE4B5', 'rgb': '255 228 181'},
          'Test': {'hex': 'F0FFFF', 'rgb': '240 255 255'},
          'Tornado Warning': {'hex': 'FF0000', 'rgb': '255 0 0'},
          'Tornado Watch': {'hex': 'FFFF00', 'rgb': '255 255 0'},
          'Tropical Depression Local Statement': {'hex': 'FFE4B5',
                                                  'rgb': '255 228 181'},
          'Tropical Storm Local Statement': {'hex': 'FFE4B5',
                                             'rgb': '255 228 181'},
          'Tropical Storm Warning': {'hex': 'B22222', 'rgb': '178 34 34'},
          'Tropical Storm Watch': {'hex': 'F08080', 'rgb': '240 128 128'},
          'Tsunami Advisory': {'hex': 'D2691E', 'rgb': '210 105 30'},
          'Tsunami Warning': {'hex': 'FD6347', 'rgb': '253 99 71'},
          'Tsunami Watch': {'hex': 'FF00FF', 'rgb': '255 0 255'},
          'Typhoon Local Statement': {'hex': 'FFE4B5', 'rgb': '255 228 181'},
          'Typhoon Warning': {'hex': 'DC143C', 'rgb': '220 20 60'},
          'Typhoon Watch': {'hex': 'FF00FF', 'rgb': '255 0 255'},
          'Urban and Small Stream Flood Advisory': {'hex': '00FF7F',
                                                    'rgb': '0 255 127'},
          'Volcano Warning': {'hex': '2F4F4F', 'rgb': '47 79 79'},
          'Wind Advisory': {'hex': 'D2B48C', 'rgb': '210 180 140'},
          'Wind Chill Advisory': {'hex': 'AFEEEE', 'rgb': '175 238 238'},
          'Wind Chill Warning': {'hex': 'B0C4DE', 'rgb': '176 196 222'},
          'Wind Chill Watch': {'hex': '5F9EA0', 'rgb': '95 158 160'},
          'Winter Storm Warning': {'hex': 'FF69B4', 'rgb': '255 105 180'},
          'Winter Storm Watch': {'hex': '4682B4', 'rgb': '70 130 180'},
          'Winter Weather Advisory': {'hex': '7B68EE', 'rgb': '123 104 238'}
          }