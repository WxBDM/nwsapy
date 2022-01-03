Data Validation Tables
======================

.. _dvt:

.. currentmodule:: nwsapy.NWSAPy

Data Validation Tables are designed to provide a snapshot of the parameters
that are valid and will not kick back an error from the NWS API.

For instance, suppose you are getting all active tornado alerts:

.. code-block:: python

	tors = api_connector.get_active_alerts(event = 'Tornado')

This will not work, as ``Tornado`` is not in the :ref:`Events <Product DVT>`
Data Validation Table. NWSAPy will raise a ``DataValidationError`` and tell you
that it is not found in the respective Data Validation Table.
However, ``Tornado Warning`` and ``Tornado Watch`` are in the Data Validation 
Table associated with this parameter, so instead you'll read in your parameter as 
such:

.. code-block:: python

	tors = api_connector.get_active_alerts(event = ['Tornado Warning', 'Tornado Watch'])

This section provides all the Data Validation Tables, as well as what methods
they are used in to validate your input. In addition, each parameter listing in the
NWSAPy API reference has a link to the respective table it uses to check to ensure
that the data is valid.

.. warning::
	You *must* pay attention to capitalization and spellig when building parameters
	for your ``get_*`` functions, as the API may say it's invalid. NWSAPy will,
	in the very near future, will handle any capitalization errors and allow
	for a more robust parameter system (for a lack of better words).

.. _Area DVT:

Area
----

This data validation table is used in the following methods:

- :meth:`get_active_alerts`
- :meth:`get_alerts`
- :meth:`get_alert_by_area`

.. table:: Valid Areas

	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| AL             | Alabama              | MA             | Massachussetts | TX             | Texas                           |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| AK             | Alaska               | MI             | Michigan       | UT             | Utah                            |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| AS             | American Samoa       | MN             | Minnesota      | VT             | Vermont                         |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| AR             | Arkansas             | MS             | Mississippi    | VI             | Virgin Islands                  |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| AZ             | Arizona              | MO             | Missouri       | VA             | Virginia                        |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| CA             | California           | MT             | Montana        | WA             | Washington                      |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| CO             | Colorado             | NE             | Nebraska       | WV             | West Virginia                   |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| CT             | Connecticut          | NV             | Nevada         | WI             | Wisconsin                       |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| DE             | Deleware             | NH             | New Hampshire  | WY             | Wyoming                         |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| DC             | District of Columbia | NJ             | New Jersey     | PZ             | Eastern North Pacific Ocean     |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| FL             | Florida              | NM             | New Mexico     | PK             | North Pacific Ocean Near Alaska |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| GA             | Georiga              | NY             | New York       | PH             | Central Pacific Ocean           |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| GU             | Guam                 | NC             | North Carolina | PS             | South Central Pacific Ocean     |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| HI             | Hawaii               | ND             | North Dakota   | PM             | Western Pacific Ocean           |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| ID             | Idaho                | OH             | Ohio           | AN             | Northwest North Atlantic Ocean  |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| IL             | Illinois             | OK             | Oklahoma       | AM             | West North Atlantic Ocean       |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| IN             | Indiana              | OR             | Oregon         | GM             | Gulf of Mexico                  |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| IA             | Iowa                 | PA             | Pennsylvania   | LS             | Lake Superior                   |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| KS             | Kansas               | PR             | Puerto Rico    | LM             | Lake Michigan                   |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| KY             | Kentucky             | RI             | Rhode Island   | LH             | Lake Huron                      |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| LA             | Louisiana            | SC             | South Carolina | LC             | Lake St. Clair                  |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| ME             | Maine                | SD             | South Dakota   | LE             | Lake Erie                       |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+
	| MD             | Maryland             | TN             | Tennessee      | LO             | Lake Ontario                    |
	+----------------+----------------------+----------------+----------------+----------------+---------------------------------+

.. _Certainty DVT:

Certainty
---------

This data validation table is used in the following methods: 

- :meth:`get_active_alerts`
- :meth:`get_alerts`

.. table:: Valid Certainty Levels

	+--------+----------+----------+----------+---------+
	| likely | observed | possible | unlikely | unknown |
	+--------+----------+----------+----------+---------+

.. _Marine DVT:

Marine Regions
--------------

This data validation table is used in the following methods:

- :meth:`get_active_alerts`
- :meth:`get_alerts`
- :meth:`get_alert_by_marine_region`

.. table:: Valid Marine Regions

	+----+-----------------+
	| AL | Alaska Region   |
	+----+-----------------+
	| AT | Atlantic Region |
	+----+-----------------+
	| GL | Great Lakes     |
	+----+-----------------+
	| GM | Gulf of Mexico  |
	+----+-----------------+
	| PA | Pacific Region  |
	+----+-----------------+
	| PI | Pacific Islands |
	+----+-----------------+

.. _Message Types DVT:

Message Types
-------------

This data validation table is used in the following methods: 

- :meth:`get_active_alerts`
- :meth:`get_alerts`

.. table:: Valid Message Types

	+-------+--------+--------+
	| Alert | Cancel | Update | 
	+-------+--------+--------+


.. _Product DVT:

Products (Event)
----------------

This data validation table is used in the following methods:

- :meth:`get_active_alerts`
- :meth:`get_alerts`
  
.. table:: Valid Alert Products (Event)

	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| 911 Telephone Outage Emergency         | Extreme Cold Watch           | High Wind Watch                         | Small Craft Advisory For Rough Bar    |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Administrative Message                 | Extreme Fire Danger          | Hurricane Force Wind Warning            | Small Craft Advisory For Winds        |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Air Quality Alert                      | Extreme Wind Warning         | Hurricane Force Wind Watch              | Small Stream Flood Advisory           |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Air Stagnation Advisory                | Fire Warning                 | Hurricane Local Statement               | Snow Squall Warning                   |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Arroyo And Small Stream Flood Advisory | Fire Weather Watch           | Hurricane Warning                       | Special Marine Warning                |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Ashfall Advisory                       | Flash Flood Statement        | Hurricane Watch                         | Special Weather Statement             |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Ashfall Warning                        | Flash Flood Warning          | Hydrologic Advisory                     | Storm Surge Warning                   |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Avalanche Advisory                     | Flash Flood Watch            | Hydrologic Outlook                      | Storm Surge Watch                     |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Avalanche Warning                      | Flood Advisory               | Ice Storm Warning                       | Storm Warning                         |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Avalanche Watch                        | Flood Statement              | Lake Effect Snow Advisory               | Storm Watch                           |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Beach Hazards Statement                | Flood Warning                | Lake Effect Snow Warning                | Test                                  |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Blizzard Warning                       | Flood Watch                  | Lake Effect Snow Watch                  | Tornado Warning                       |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Blizzard Watch                         | Freeze Warning               | Lake Wind Advisory                      | Tornado Watch                         |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Blowing Dust Advisory                  | Freeze Watch                 | Lakeshore Flood Advisory                | Tropical Depression Local Statement   |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Blowing Dust Warning                   | Freezing Fog Advisory        | Lakeshore Flood Statement               | Tropical Storm Local Statement        |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Brisk Wind Advisory                    | Freezing Rain Advisory       | Lakeshore Flood Warning                 | Tropical Storm Warning                |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Child Abduction Emergency              | Freezing Spray Advisory      | Lakeshore Flood Watch                   | Tropical Storm Watch                  |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Civil Danger Warning                   | Frost Advisory               | Law Enforcement Warning                 | Tsunami Advisory                      |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Civil Emergency Message                | Gale Warning                 | Local Area Emergency                    | Tsunami Warning                       |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Coastal Flood Advisory                 | Gale Watch                   | Low Water Advisory                      | Tsunami Watch                         |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Coastal Flood Statement                | Hard Freeze Warning          | Marine Weather Statement                | Typhoon Local Statement               |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Coastal Flood Warning                  | Hard Freeze Watch            | Nuclear Power Plant Warning             | Typhoon Warning                       |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Coastal Flood Watch                    | Hazardous Materials Warning  | Radiological Hazard Warning             | Typhoon Watch                         |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Dense Fog Advisory                     | Hazardous Seas Warning       | Red Flag Warning                        | Urban And Small Stream Flood Advisory |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Dense Smoke Advisory                   | Hazardous Seas Watch         | Rip Current Statement                   | Volcano Warning                       |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Dust Advisory                          | Hazardous Weather Outlook    | Severe Thunderstorm Warning             | Wind Advisory                         |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Dust Storm Warning                     | Heat Advisory                | Severe Thunderstorm Watch               | Wind Chill Advisory                   |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Earthquake Warning                     | Heavy Freezing Spray Warning | Severe Weather Statement                | Wind Chill Warning                    |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Evacuation - Immediate                 | Heavy Freezing Spray Watch   | Shelter In Place Warning                | Wind Chill Watch                      |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Excessive Heat Warning                 | High Surf Advisory           | Short Term Forecast                     | Winter Storm Warning                  |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Excessive Heat Watch                   | High Surf Warning            | Small Craft Advisory                    | Winter Storm Watch                    |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Extreme Cold Warning                   | High Wind Warning            | Small Craft Advisory For Hazardous Seas | Winter Weather Advisory               |
	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+

.. _Region Type DVT:

Region Type 
-----------

This data validation table is used in the following methods:

- :meth:`get_active_alerts`
- :meth:`get_alerts`

.. table:: Valid Region Types

	+------+--------+
	| Land | Marine |
	+------+--------+

.. _Severity DVT:

Severity
--------

This data validation table is used in the following methods:

- :meth:`get_active_alerts`
- :meth:`get_alerts`

.. table:: Valid Severity

	+---------+-------+----------+--------+---------+
	| Extreme | Minor | Moderate | Severe | Unknown |
	+---------+-------+----------+--------+---------+

.. _Status DVT:

Status
------

This data validation table is used in the following methods:

- :meth:`get_active_alerts`
- :meth:`get_alerts`

.. table:: Valid Status
	
	+--------+----------+-------+--------+------+
	| Actual | Exercise | Draft | System | Test |
	+--------+----------+-------+--------+------+

.. _Urgency DVT:

Urgency
-------

This data validation table is used in the following methods:

- :meth:`get_active_alerts`
- :meth:`get_alerts`

.. table:: Valid Urgency

	+----------+--------+-----------+------+---------+
	| Expected | Future | Immediate | Past | Unknown |
	+----------+--------+-----------+------+---------+
