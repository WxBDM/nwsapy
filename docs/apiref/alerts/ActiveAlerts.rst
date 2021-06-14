Active Alerts
=============

Introduction: Active Alerts
---------------------------
To get all active alerts, use:

.. code-block:: python

    nwsapy.get_active_alerts()

This will return an ``ActiveAlerts`` object, as described in the API reference below. This is equivalent to the all alerts endpoint code: ``nwsapy.get_all_alerts(active = True)``.

The ``ActiveAlert`` object is iterable and indexable:

.. code-block:: python

    svr_tstorms = nwsapy.get_active_alerts(event = "Severe Thunderstorm Warning")

    for warning in svr_tstorms:
        print(warning.headline)

    first_warning = svr_tstorms[0]

Example Usage: Active Alerts
----------------------------
This section provides a few examples on using ``nwsapy.get_active_alerts()``, as well as an example using the individual alerts. To see more examples with using individual alerts, see the Individual Alerts page.

Using parameters: Active Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If we wanted to get a pandas dataframe of all of the active excessive heat warnings in Utah:

.. code-block:: python

    excessive_heat_warnings = nwsapy.get_active_alerts(active = True, event = "Excessive Heat Warning", area = "UT")
    df = excessive_heat_warnings.to_dataframe()

>>> print(df)
                                                 @id  ...   urgency
0  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
1  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
2  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
[3 rows x 33 columns]

Conflicting Parameters: Active Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One thing to note, however, is that if you have 2 conflicting parameters (which are ``area``, ``point``, ``region``, ``region_type``, and ``zone``), you will get an error:

>>> excessive_heat_warnings = nwsapy.get_all_alerts(active = True, area = "UT", region_type = "land")
ValueError: Incompatible parameters, ensure only one exists: area, point, region, region_type, zone

Multiple Events: Active Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

But for some reason, it interests you to have not only the excessive heat warnings, but also the severe thunderstorm warnings. You can do so as such:

.. code-block:: python

    warnings = nwsapy.get_all_alerts(active = True, event = ["Severe Thunderstorm Warning", "Excessive Heat Warning"])

But now, you're only interested in these events only in Utah and Ohio:

.. code-block:: python

    warnings = nwsapy.get_all_alerts(active = True, event = ["Severe Thunderstorm Warning", "Excessive Heat Warning"], area = ["OH", "UT"])

This will get you all severe thunderstorm warnings and excessive heat warnings in both Ohio and Utah.

API Reference: Active Alerts
----------------------------

Method: get_active_alerts
^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: nwsapy
.. automethod:: nwsapy.get_active_alerts(area, certainty, event, limit, message_type, point, region, region_type, severity, status, urgency, zone)

Class: alerts.ActiveAlerts
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.alerts.ActiveAlerts( )
	:inherited-members:
	:members: