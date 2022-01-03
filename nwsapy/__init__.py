# -*- coding: utf:8 -*-
"""
NWSAPy
======
::

     _   _  __          __   _____              _____          
    | \ | | \ \        / /  / ____|     /\     |  __ \         
    |  \| |  \ \  /\  / /  | (___      /  \    | |__) |  _   _ 
    | . ` |   \ \/  \/ /    \___ \    / /\ \   |  ___/  | | | |
    | |\  |    \  /\  /     ____) |  / ____ \  | |      | |_| |
    |_| \_|     \/  \/     |_____/  /_/    \_\ |_|       \__, |
                                                          __/ |
                                                         |___/ 


A pythonic implementation of the National Weather Service API. It's designed
to do the following:

    1) Maintain clean, simplistic, minimal, and consistent user-end code.
    2) Construct URL's and request data on your behalf
    3) Minimize possible errors while fetching (GET) data from the API.

:copyright: (c) 2021 by Brandon D. Molyneaux.
:license: Apache 2.0, see LICENSE.txt for more details.

Links
-----
- GitHub:     https://github.com/WxBDM/nwsapy
- Docs:       https://nwsapy.readthedocs.io/en/latest/
- NWS API:    https://www.weather.gov/documentation/services-web-api

Examples
--------
Almost all API requests will be of this format: 

.. code-block:: python
    
    from nwsapy import api_connector
    api_connector.set_user_agent("My App", "My website/email")
    variable = api_connector.get_*(**kwargs)

Note that the ``set_user_agent`` is required by the API - this is for the 
National Weather Service API maintainers to contact you in the event of a
security issue. NWSAPy does NOT retain this information and will not be seen
by anyone on the NWSAPy team.

A simple example getting all tornado warnings and putting them into a Pandas
Dataframe:

.. code-block:: python

    from nwsapy import api_connector

    # Set the request information - required by the API.
    api_connector.set_user_agent("My Application", "My website/email")

    # Get all of the active tornado warnings.
    active_tornado_warnings = api_connector.get_active_alerts(event = 'Tornado Warning')

    # Convert it into a dataframe
    df = active_tor_warnings.to_dataframe()
    
"""

from nwsapy.entrypoint import NWSAPy
nwsapy = api_connector = NWSAPy() # leaving this here for backwards compatability