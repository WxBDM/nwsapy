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

Functions and Objects Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

When an alerts object is given to you, there's an internal list (generally can be called by ``.alerts``) containing the individual alerts. However, each alert data type is based upon the type of alert it is. For example, an alert for a Frost Advisory would be a ``frostadvisory`` object (that is, if you were to call ``type`` on the object, it would return ``frostadvisory``). Similarily, a tornado warning alert object would be ``tornadowarning``.

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

This specific alert would have the following attributes from the ``properties`` portion:

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
	
When it comes to geometry (found in the ``geometry`` portion), things are handled slightly differently. That is, the coordinates are converted into shapely polygons and points. So, the attributes from this would be:

	| ``.polygon``
	| ``.points``
	| ``.point_collection``

Note that if there is no geometry associated with the alert, these attributes will not be added.

Individual objects will vary depending upon the type of object and which method it's being called from, as the National Weather Service API is structured slightly differently. For now, to see what attributes the alert object has is to call ``dir()`` on it.

Examples
^^^^^^^^

No examples yet. Stay tuned.



