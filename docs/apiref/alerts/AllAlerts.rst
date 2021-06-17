All Alerts
==========

.. currentmodule:: nwsapy

Introduction: All Alerts
------------------------
To get all alerts, use:

.. code-block:: python

    nwsapy.get_all_alerts()

This will return an ``AllAlerts`` object, as described in the API reference below.

The ``AllAlerts`` object is iterable and indexable:

.. code-block:: python

    all_floods = nwsapy.get_all_alerts(event = "Flash Flood Warning")

    for flood in all_floods:
        print(flood.headline)

    first_flood_warning = all_floods[0]

Note: as of v0.2.0, the start and end times are not implemented. This will hopefully be implemented in the future.

The methods that are implemented for :class:`AllAlerts` are::

    to_dataframe()
    to_dict()

This endpoint in the NWS API does take parameters. As such, APy provides a way to use these parameters in a pythonic manner to reduce server latency. See the API reference for details on the various parameters and the data types/structures associated with them. Note that APy does include data type and structure checking to minimize 404 errors from the API.

Example Usage: All Alerts
-------------------------
This section provides a few examples on using ``nwsapy.get_all_alerts()``, as well as an example using the individual alerts. To see more examples with using individual alerts, see the Individual Alerts page.

Using parameters: All Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you wanted to get a DataFrame of the excessive heat warnings in Utah:

.. code-block:: python

    excessive_heat_warnings = nwsapy.get_all_alerts(event = "Excessive Heat Warning", area = "UT")
    df = excessive_heat_warnings.to_dataframe()

>>> print(df)
                                                  @id  ...                                         replacedBy
0   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...                                                NaN
1   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...                                                NaN
2   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...                                                NaN
3   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
4   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
5   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
6   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
7   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
8   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
9   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
10  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
11  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  https://api.weather.gov/alerts/urn:oid:2.49.0....
[12 rows x 35 columns]

Similar methods: All Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This section outlines methods that are equivalent.

.. code-block:: python

    # Getting the active alerts
    nwsapy.get_all_alerts(active = True)
    nwsapy.get_active_alerts()

    # All alerts in Alabama
    nwsapy.get_all_alerts(area = "AL")
    nwsapy.get_alert_by_area("AL")

    # All alerts in the Gulf of Mexico
    nwsapy.get_all_alerts(region = "GM")
    nwsapy.get_alert_by_marine_region("GM")

    # All alerts in the OKC037 area.
    nwsapy.get_all_alerts(zone = "OKC037")
    nwsapy.get_alert_by_zone("OKC037")

For example, we can either call ``get_active_alerts`` with the same parameters or include ``active = True`` in the parameters:

.. code-block:: python

    excessive_heat_warnings = nwsapy.get_all_alerts(active = True, event = "Excessive Heat Warning", area = "UT")
    df = excessive_heat_warnings.to_dataframe()

>>> print(df)
                                                 @id  ...   urgency
0  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
1  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
2  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
[3 rows x 33 columns]

Likewise, with alert by area:

.. code-block:: python

    excessive_heat_warnings = nwsapy.get_all_alerts(active = True, event = "Excessive Heat Warning", area = "UT")
    df = excessive_heat_warnings.to_dataframe()

Conflicting Parameters: All Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One thing to note, however, is that if you have 2 conflicting parameters (which are ``area``, ``point``, ``region``, ``region_type``, and ``zone``), you will get an error:

>>> excessive_heat_warnings = nwsapy.get_all_alerts(active = True, area = "UT", region_type = "land")
ValueError: Incompatible parameters, ensure only one exists: area, point, region, region_type, zone

Getting Individual Alerts: All Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now suppose you wanted to work with individual alerts to see which severe thunderstorm warning expires last:

.. code-block:: python

    svr_tstorm = nwsapy.get_all_alerts(active = True, event = "Severe Thunderstorm Warning")
    svr_tstorm_expires = [alert.expires for alert in svr_tstorm]
    svr_tstorm_expires_reversed = list(reversed(sorted(svr_tstorm_expires)))

>>> print(svr_tstorm_expires)
[datetime.datetime(2021, 6, 13, 13, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000))), datetime.datetime(2021, 6, 13, 12, 15, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400)))]
>>> print(svr_tstorm_expires_reversed)
[datetime.datetime(2021, 6, 13, 12, 15, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))), datetime.datetime(2021, 6, 13, 13, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))]

For more examples on working with the Individual Alerts, see the Individual Alerts page.

Multiple Events: All Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

But for some reason, it interests you to have not only the excessive heat warnings, but also the severe thunderstorm warnings. You can do so as such:

.. code-block:: python

    warnings = nwsapy.get_all_alerts(active = True, event = ["Severe Thunderstorm Warning", "Excessive Heat Warning"])

But now, you're only interested in these events only in Utah and Ohio:

.. code-block:: python

    warnings = nwsapy.get_all_alerts(active = True, event = ["Severe Thunderstorm Warning", "Excessive Heat Warning"], area = ["OH", "UT"])

This will get you all severe thunderstorm warnings and excessive heat warnings in both Ohio and Utah.

API Reference: All Alerts
-------------------------
As of v0.2.0, **all parameters are case sensitive**. If you receive an error, it is likely due to this.

.. important::
    Note that the parameters ``area``, ``point``, ``region``, ``region_type``, and ``zone`` are incompatible with each other.

    That is, you cannot do: ``nwsapy.get_all_alerts(region_type = "land", area = "FL")``.

Method: get_all_alerts
^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: nwsapy.NWSAPy.get_all_alerts(active, area, certainty, end, event, limit, message_type, point, region, region_type, severity, start, status, urgency, zone)

Class: AllAlerts
^^^^^^^^^^^^^^^^
.. autoclass:: nwsapy.alerts.AllAlerts( )
    :inherited-members:
    :members:

