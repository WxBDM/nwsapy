Alerts
======

The alerts module retrieves information from ``/alerts/...``. More specifically, this provides objects for the following urls:

	| ``/alerts``
	| ``/alerts/active``
	| ``/alerts/types``
	| ``/alerts/{id}``
	| ``/alerts/active/count``
	| ``/alerts/active/zone/{zoneId}``
	| ``/alerts/active/area/{area}``
	| ``/alerts/active/region/{region}``

API URL Path
------------

The following table shows all alert-related NWSAPy functions are and what the equivalent API URL path it is.

+---------------------------------------------+------------------------------------+-------------------------------------+
| NWSAPy Function                             | Equivalent NWS API path            | Associated Alert Object             |
+=============================================+====================================+=====================================+
| :meth:`nwsapy.get_all_alerts()`             | ``/alerts``                        | :class:`alerts.AllAlerts`           |
+---------------------------------------------+------------------------------------+-------------------------------------+
| :meth:`nwsapy.get_active_alerts()`          | ``/alerts/active``                 | :class:`alerts.ActiveAlerts`        |
+---------------------------------------------+------------------------------------+-------------------------------------+
| :meth:`nwsapy.get_alert_types()`            | ``/alerts/types``                  | :class:`alerts.AlertTypes`          |
+---------------------------------------------+------------------------------------+-------------------------------------+
| :meth:`nwsapy.get_alert_by_id()`            | ``/alerts/{id}``                   | :class:`alerts.AlertById`           |
+---------------------------------------------+------------------------------------+-------------------------------------+
| :meth:`nwsapy.get_alert_count()`            | ``/alerts/active/count``           | :class:`alerts.AlertByCount`        |
+---------------------------------------------+------------------------------------+-------------------------------------+
| :meth:`nwsapy.get_alert_by_zone()`          | ``/alerts/active/zone/{zoneId}``   | :class:`alerts.AlertByZone`         |
+---------------------------------------------+------------------------------------+-------------------------------------+
| :meth:`nwsapy.get_alert_by_area()`          | ``/alerts/active/area/{area}``     | :class:`alerts.AlertByArea`         |
+---------------------------------------------+------------------------------------+-------------------------------------+
| :meth:`nwsapy.get_alert_by_marine_region()` | ``/alerts/active/region/{region}`` | :class:`alerts.AlertByMarineRegion` |
+---------------------------------------------+------------------------------------+-------------------------------------+

For example, if you would like to retrieve the alert types from ``/alerts/types``, you would call :meth:`nwsapy.get_alert_types()`. This would then return an object containing the information from the API in an :class:`alerts.AlertTypes` object. See Individual Alerts for more information.


Examples Using the Alerts
-------------------------

.. _alerts_example_1:

**Example 1:** ``nwsapy.get_active_alerts()``

Let's suppose we're looking to see if a certain city has some kind of alert issued for it.

.. code-block:: python

	import nwsapy
	from shapely.geometry import Point

	# Lat/Lon for Arthur, NE.
	arthur = Point([-101.6916, 41.5717])  # create a shapely point
	all_alerts = nwsapy.get_active_alerts()  # retrieves all active alerts.

	for alert in all_alerts: # iterate through the alerts to see if NYC is in any of these alerts.
	    if alert.event == "Test Message": # There's always a test message, ignore it.
	        continue

	    if alert.polygon is not None:  # Ensure there is a polygon since we are looking at lat/lon coordinates.
	        is_in = arthur.within(alert.polygon)  # check to see if NYC is in the alert's polygon.
	        issue_time = alert.sent.strftime("%H:%M:%S on %m/%d/%Y")  # extract the sent time from the alert.
	        expire = alert.expires.strftime("%H:%M:%S on %m/%d/%Y") # extract the expiration from the alert.
			
	        if is_in: # if it's in, print a successful message!
	            print(f'Aurthur, NE is in the {alert.event} sent by {alert.senderName} at {issue_time}, expires at: {expire}')
	        else:  # If not, then print an unsuccessful message.
	            print(f'Aurthur, NE is not in the {alert.event} sent by {alert.senderName} at {issue_time}, expires at: {expire}')

If the output were to be shown, it would take up a lot of space; there's over 200 alerts. If we use ``filter_by()``, we can filter by the alert that we want:

.. code-block:: python

	...
	# Lat/Lon for Arthur, NE.
	arthur = Point([-101.6916, 41.5717])  # create a shapely point
	all_alerts = nwsapy.get_active_alerts()  # retrieves all active alerts.
	all_severe_tstorm_warnings = all_alerts.filter_by("Severe Thunderstorm Warning")
	
	for alert in all_severe_tstorm_warnings:
		...

This will give us this result:

>>> Aurthur, NE is in the Severe Thunderstorm Warning sent by NWS North Platte NE at 16:13:00 on 05/13/2021, expires at: 16:45:00 on 05/13/2021
>>> Aurthur, NE is not in the Severe Thunderstorm Warning sent by NWS Miami FL at 18:11:00 on 05/13/2021, expires at: 19:15:00 on 05/13/2021

In 2 lines of code, we were able to (1) fetch all of the current alerts and (2) filter by the type of warning we want. After that, it's just a matter of iterating through all of the alerts and checking to see if Arthur, NE is in the severe thunderstorm warning.

At the time of making this example, there was also a severe thunderstorm warning in Florida. Out of curiosity, who sent out the first alert? Let's check:

.. code-block:: python

	import nwsapy

	all_alerts = nwsapy.get_active_alerts()  # retrieves all active alerts.
	svr_tstorms = all_alerts.filter_by('severe thunderstorm warning')

	svr_storm1 = svr_tstorms[0]
	svr_storm2 = svr_tstorms[1]

	if svr_storm1.sent_before(svr_storm2):
	    print(f"{svr_storm1.senderName} has sent out a severe warning before {svr_storm2.senderName} has!")
	else:
	    print(f"{svr_storm2.senderName} has sent out a severe warning before {svr_storm1.senderName} has!")

Gives the following result:

>>> NWS Goodland KS has sent out a severe warning before NWS Miami FL has!

DataValidationError Tables
--------------------------

When developing, you may encounter a ``DataValidationError``. This error states that the data that is being read in is not a valid data point in the API. This section provides a reference of what data is valid based upon the function that is called. The error, when raised, should provide a link to the appropriate table for easy referencing.

.. _alerts_by_area_table_validation:
.. table:: Alerts by Area 

	+----------------------------------------------------------------------------------------------------------------------------+
	|                                        Function: :meth:`nwsapy.get_alert_by_area()`                                        |
	+================+======================+================+================+================+=================================+
	| **Valid Data** | **Description**      | **Valid Data** | **Description**| **Valid Data** | **Description**                 |
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

|

.. _alerts_by_marine_table_validation:
.. table:: Alerts by Marine Region

	+-------------------------------------------------------+
	| Function: :meth:`nwsapy.get_alert_by_marine_region()` |
	+======================+================================+
	| **Valid Data**       | **Description**                |
	+----------------------+--------------------------------+
	| AL                   | Alaska Region                  |
	+----------------------+--------------------------------+
	| AT                   | Atlantic Region                |
	+----------------------+--------------------------------+
	| GL                   | Great Lakes                    |
	+----------------------+--------------------------------+
	| GM                   | Gulf of Mexico                 |
	+----------------------+--------------------------------+
	| PA                   | Pacific Region                 |
	+----------------------+--------------------------------+
	| PI                   | Pacific Islands                |
	+----------------------+--------------------------------+

|

.. _valid_nws_alert_products:
.. table:: Valid Alert Products

	+----------------------------------------+------------------------------+-----------------------------------------+---------------------------------------+
	| Valid NWS Alert Products: used when ``.count()`` and ``.filter_by()`` are called.                                                                       |
	+========================================+==============================+=========================================+=======================================+
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

.. toctree::
	:hidden:
	:maxdepth: 1
	
	Individual Alerts <IndividualAlerts/IndividualAlerts>
	alerts.AllAlerts <AllAlerts/AllAlerts>
	alerts.ActiveAlerts <ActiveAlerts/ActiveAlerts>
	alerts.AlertType <AlertTypes/AlertTypes>
	alerts.AlertById <AlertById/AlertById>
	alerts.AlertByCount <AlertByCount/AlertByCount>
	alerts.AlertByZone <AlertByZone/AlertByZone>
	alerts.AlertByArea <AlertByArea/AlertByArea>
	alerts.AlertByMarineRegion <AlertByMarineRegion/AlertByMarineRegion>
