"""This file is intended to be a mapping to some of the more common
meteorological/geography things."""

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
        'WI' : 'Wisconsin', 'WY' : 'Wyoming'}

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
            'Wisconsin': 'WI', 'Wyoming': 'WY'}


def state_abbreviation_to_full_name(abbr):
    """Converts a 2 letter state abbreviation to the respective full name.

    Example: 'ND' will return 'North Dakota'
    
    :param abbr: The 2 letter abbreviation for a state.
    :returns: Full name corresponding to the parameter.
    """
    abbr_upper = abbr.upper() # transform it to uppercase
    if abbr not in abbr_state:
        e_msg = f'{abbr} not found in 2 letter abbreviation of states.'
        raise ValueError(e_msg)
    
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
        raise ValueError(e_msg)
    
    return full_state[full_title]
