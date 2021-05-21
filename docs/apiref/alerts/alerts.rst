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

.. module:: nwsapy

+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| NWSAPy Method                                      | Associated Alert Object             | Description                               |
+====================================================+=====================================+===========================================+
| :meth:`nwsapy.get_all_alerts()`                    | :class:`alerts.AllAlerts`           | Retrieves all alerts.                     |
+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| :meth:`nwsapy.get_active_alerts()`                 | :class:`alerts.ActiveAlerts`        | Retrieves active alerts.                  |
+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| :meth:`nwsapy.get_alert_types()`                   | :class:`alerts.AlertTypes`          | Retrieves types of alerts.                |
+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| :meth:`nwsapy.get_alert_by_id()`                   | :class:`alerts.AlertById`           | Retrieves alerts by ID.                   |
+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| :meth:`nwsapy.get_alert_count()`                   | :class:`alerts.AlertByCount`        | Retrieves the number of alerts.           |
+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| :meth:`nwsapy.get_alert_by_zone()`                 | :class:`alerts.AlertByZone`         | Retrieves alerts by a zone.               |
+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| :meth:`nwsapy.get_alert_by_area()`                 | :class:`alerts.AlertByArea`         | Retrieves alerts by an area (land or sea).|
+----------------------------------------------------+-------------------------------------+-------------------------------------------+
| :meth:`nwsapy.get_alert_by_marine_region()`        | :class:`alerts.AlertByMarineRegion` | Retrieves alerts by marine region.        |
+----------------------------------------------------+-------------------------------------+-------------------------------------------+

For example, if you would like to retrieve the alert types from ``/alerts/types``, you would call :meth:`nwsapy.get_alert_types()`. This would then return an object containing the information from the API in an :class:`alerts.AlertTypes` object. See Individual Alerts for more information.


All Alert objects are...
------------------------

- Iterable

.. code-block:: python

	all_alerts = nwsapy.get_all_alerts()
	
	for alert in all_alerts:
		print(alert.headline)

- Indexable

.. code-block:: python

	all_alerts = nwsapy.get_all_alerts()
	
	print(all_alerts[1])
	print(all_alerts[-1])


Examples Using the Alerts
-------------------------

.. _alerts_example_1:

**Example 1:** :meth:`nwsapy.nwsapy.get_active_alerts()`

Let's suppose we're looking to see if a certain city has some kind of alert issued for it.

.. code-block:: python

	from nwsapy import nwsapy
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


.. toctree::
	:hidden:
	:maxdepth: 1
	
	Data Validation Tables <datavalidationtables>
	Individual Alerts <IndividualAlerts/IndividualAlerts>
	alerts.AllAlerts <AllAlerts/AllAlerts>
	alerts.ActiveAlerts <ActiveAlerts/ActiveAlerts>
	alerts.AlertType <AlertTypes/AlertTypes>
	alerts.AlertById <AlertById/AlertById>
	alerts.AlertByCount <AlertByCount/AlertByCount>
	alerts.AlertByZone <AlertByZone/AlertByZone>
	alerts.AlertByArea <AlertByArea/AlertByArea>
	alerts.AlertByMarineRegion <AlertByMarineRegion/AlertByMarineRegion>
