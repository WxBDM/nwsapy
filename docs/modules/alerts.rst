Alerts Module
=============

The alerts module retrieves information from ``/alerts/...``. More specifically, this module provides objects for the following urls:

	| ``/alerts``
	| ``/alerts/active``
	| ``/alerts/types``
	| ``/alerts/{id}``
	| ``/alerts/active/count``
	| ``/alerts/active/zone/{zoneId}``
	| ``/alerts/active/area/{area}``
	| ``/alerts/active/region/{region}``

API URL Path
^^^^^^^^^^^^

The following table shows what function you should call (NWSAPy Function), what object type it returns, and what the equivalent NWS API URL path is.

+---------------------------------------------+------------------------------------+------------------------------------+
| NWSAPy Function                             | Alerts Object Type                 | Equivalent NWS API path            |
+---------------------------------------------+------------------------------------+------------------------------------+
| :meth:`nwsapy.get_active_alerts()`          | :meth:`alerts.ActiveAlerts`        | ``/alerts/active``                 |
+---------------------------------------------+------------------------------------+------------------------------------+
| :meth:`nwsapy.get_alert_by_id()`            | :meth:`alerts.AlertById`           | ``/alerts/{id}``                   |
+---------------------------------------------+------------------------------------+------------------------------------+
| :meth:`nwsapy.get_alert_by_marine_region()` | :meth:`alerts.AlertByMarineRegion` | ``/alerts/active/region/{region}`` |
+---------------------------------------------+------------------------------------+------------------------------------+
| :meth:`nwsapy.get_alert_by_area()`          | :meth:`alerts.AlertByArea`         | ``/alerts/active/area/{area}``     |
+---------------------------------------------+------------------------------------+------------------------------------+
| :meth:`nwsapy.get_alert_count()`            | :meth:`alerts.AlertByCount`        | ``alerts/active/count``            |
+---------------------------------------------+------------------------------------+------------------------------------+

**Note**: You don't want to retrieve the alert object manually. Use the built in functions as described above.

Individual Alerts
^^^^^^^^^^^^^^^^^

When an alerts object is given to you, there's an internal list (can be called by ``.alerts``) containing the individual alerts. Each of these indivual alerts are an object. Thus, ``.alerts`` is a list of individual alert objects. The type is based upon the type of alert it is. For example, an alert for a Frost Advisory would be a ``frostadvisory`` object (that is, if you were to call ``type`` on the object, it would return ``frostadvisory``). Similarily, a tornado warning alert object would be ``tornadowarning``.

.. important:: Each alert that is dynamically created is different depending upon which function is called. Due to this, it is very difficult to document properly. In the API Reference section (both full and here), the methods for the individual alerts are documented. In order to see the attributes, it is recommended to call ``dir`` on the object. The documentation for these dynamically created alerts are located :ref:`here<dynamically-created-alerts>`.

Each alert property is stored as an attribute. So, for example, let's say that we are looking at the following special marine warning in the API web page (note that a lot of information is removed for simplicity). We would expect to see something like this:

.. code-block::

	{
	    "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -80.780000000000001,
                            30.129999999999999
                        ],
                        [
                            -81,
                            31.02
                        ],
                        [
                            -80.349999999999994,
                            30.27
                        ],
                        [
                            -80.780000000000001,
                            30.129999999999999
                        ]
                    ]
                ]
            },
	    "properties": {
	        "id": "urn:oid:2.49.0.1.840.0.8dfe228cd0a56af826ab6d7fbc3f40ba82eac48c.002.1",
	        "areaDesc": "Coastal waters from Fernandina Beach to St. Augustine FL out 20 NM; Waters from Altamaha Sound GA to Fernandina Beach FL from 20 to 60 NM; Waters from Fernandina Beach to St. Augustine FL from 20 to 60 NM",
	        "effective": "2021-05-12T17:30:00-04:00",
	        "expires": "2021-05-12T18:45:00-04:00",
	        "status": "Actual",
	        "messageType": "Update",
	        "severity": "Severe",
	        "event": "Special Marine Warning",
	        "senderName": "NWS Jacksonville FL",
	        "headline": "Special Marine Warning issued May 12 at 5:30PM EDT until May 12 at 6:45PM EDT by NWS Jacksonville FL",
	        "description": "For the following areas...\nCoastal waters from Fernandina Beach to St. Augustine FL out 20 NM...\nWaters from Altamaha Sound GA to Fernandina Beach FL from 20 to 60\nNM...\nWaters from Fernandina Beach to St. Augustine FL from 20 to 60 NM...\n\nAt 529 PM EDT, showers and thunderstorms were located along a\nline extending from 20 nm southeast of R2 Tower to 23 nm east of\nGuana River State Park, moving southeast at 30 knots.\n\nHAZARD...Wind gusts 34 knots or greater.\n\nSOURCE...Radar indicated.\n\nIMPACT...Small craft could be damaged in briefly higher winds and\nsuddenly higher waves.\n\nLocations impacted include...\nBuoy Hlha, Tournament Reef, Casablanca Reef and Anna Reef.",
	    }
	}

When created, this specific alert would have the following attributes from ``geometry``:

	| ``.polygon``
	| ``.points``
	| ``.point_collection``

This specific alert would have the following attributes from ``properties``:

	| ``.id`` 
	| ``.areaDesc``
	| ``.effective``
	| ``.expires``
	| ``.status``
	| ``.messageType``
	| ``.severity``
	| ``.event``
	| ``.senderName``
	| ``.headline``
	| ``.description``

.. attention:: Unless otherwise stated below, all attributes for individual alerts are strings.

	| ``.polygon`` (shapely.Polygon)
	| ``.points`` (list of shapely.Point)
	| ``.point_collection`` (shapely.Multipoint)
	| ``.sent`` (datetime.datetime)
	| ``.effective`` (datetime.datetime)
	| ``.onset`` (datetime.datetime)
	| ``.expires`` (datetime.datetime)
	| ``.ends`` (datetime.datetime)
	
	Note that some of the above attributes could also be ``None``.

Valid Data
^^^^^^^^^^

When developing, you may encounter a ``DataValidationError``. This error states that the data that is being read in is not a valid data point in the API. This section provides a reference of what data is valid based upon the function that is called.

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
	| "AL"                 | Alaska Region                  |
	+----------------------+--------------------------------+
	| "AT"                 | Atlantic Region                |
	+----------------------+--------------------------------+
	| "GL"                 | Great Lakes                    |
	+----------------------+--------------------------------+
	| "GM"                 | Gulf of Mexico                 |
	+----------------------+--------------------------------+
	| "PA"                 | Pacific Region                 |
	+----------------------+--------------------------------+
	| "PI"                 | Pacific Islands                |
	+----------------------+--------------------------------+

|

.. _alerts_no_raise_datavalidationerror:
.. table:: Active and Alert Count

	+---------------------------------------------------------------------------+
	|            Functions that do not raise ``DataValidationError``            |
	+======================================+====================================+
	| :meth:`nwsapy.get_active_alerts()`   | :meth:`nwsapy.get_alert_count()`   |
	+--------------------------------------+------------------------------------+



Examples Using the Alerts Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _alerts_example_1:

**Example 1:** ``nwsapy.get_active_alerts()``

Let's suppose we're looking to see if a certain city has some kind of alert issued for it.

.. code-block:: python

	import nwsapy
	from shapely.geometry import Point

	# Lat/Lon for Arthur, NE.
	arthur = Point([-101.6916, 41.5717])  # create a shapely point
	all_alerts = nwsapy.get_active_alerts()  # retrieves all active alerts.

	for alert in all_alerts.alerts: # iterate through the alerts to see if NYC is in any of these alerts.
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


Alerts API Reference
^^^^^^^^^^^^^^^^^^^^

.. _dynamically-created-alerts:
.. py:class:: alerts.<Alert Event Name>

   A dynamically created alert, with ``<Alert Event Name>`` being the name of the alert.
   
   For example, if the event is a tornado warning, the name of the dynamically created alert would be ``alerts.tornadowarning``. Similarily, for a small craft advisory, it would be ``alerts.smallcraftadvisory``.
   
	.. attention:: Each alert that is dynamically created is different depending upon which command is called. Due to this, it is very difficult to document properly. Documented below are the methods for each individual alert objects, but it is recommended to use call ``dir`` on the individual alert to see their attributes.
   
	.. py:method:: sent_before(other)
	
		Compares ``self.sent`` to determine if this alert was sent before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was sent before other. ``False`` otherwise.
   
	.. py:method:: sent_after(other)

		Compares ``self.sent`` to determine if this alert was sent after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was sent after other. ``False`` otherwise.
	
	.. py:method:: effective_before(other)
	
		Compares ``self.effective`` to determine if this alert is effective before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert is effective before other. ``False`` otherwise.
   
	.. py:method:: effective_after(other)

		Compares ``self.effective`` to determine if this alert is effective after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert is effective after other. ``False`` otherwise.

	.. py:method:: onset_before(other)
	
		Compares ``self.onset`` to determine if this alert was onset before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was onset before other. ``False`` otherwise.
   
	.. py:method:: onset_after(other)

		Compares ``self.onset`` to determine if this alert was onset after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was onset after other. ``False`` otherwise.
	
	.. py:method:: expires_before(other)
	
		Compares ``self.expires`` to determine if this alert will expire before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert will expire before other. ``False`` otherwise.
   
	.. py:method:: expires_after(other)

		Compares ``self.expires`` to determine if this alert will expire after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert will expire after other. ``False`` otherwise.
   

.. autoclass:: alerts.ActiveAlerts
	:noindex:
	:inherited-members:
	:members:

.. autoclass:: alerts.AlertById
	:noindex:
	:inherited-members:
	:members:

.. autoclass:: alerts.AlertByMarineRegion
	:noindex:
	:inherited-members:
	:members:

.. autoclass:: alerts.AlertByArea
	:noindex:
	:inherited-members:
	:members:

.. autoclass:: alerts.AlertByCount
	:noindex:
	:members:

	.. note:: This does not contain the dynamically created alert objects, as it only contains a count of the active alerts.