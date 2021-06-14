Alert Count
===========

.. currentmodule:: nwsapy

Introduction: Alert Count
-------------------------
This function gives you the number of total, marine, land, area, region, and zone alerts.

.. code-block:: python

    nwsapy.get_alert_count()

This will return an ``AlertByCount`` object, as described in the API reference below. Unlike other alert objects, the ``AlertByCount`` object is not iterable and indexable.

The methods that are implemented for :class:`AllAlerts` are::

    filter_marine_regions()
    filter_land_areas()
    filter_zones()

There are no parameters set by the endpoint, thus there are no parameters for this method.

Examples: Alert Count
---------------------
Suppose we wanted to see how many alerts there are in Florida, Georgia, and Alabama:

.. code-block:: python

    count = nwsapy.get_alert_count()
    n_alerts = sum(count.filter_land_areas(["FL", "AL", "GA"]).values())

We can also do it using ``get_all_alerts()``:

.. code-block:: python

    alerts = nwsapy.get_all_alerts(area = ["This is where a list of all areas would go."])
    n_alerts = len(alerts)

But suppose we wanted to get the number of land and marine alerts. We could just simply use ``get_alert_count()``:

.. code-block:: python

    count = nwsapy.get_alert_count()
    n_alerts = sum(count.areas.values()) + sum(count.regions.values())

Similarily, we could use ``get_all_alerts()``, but we'd end up making 2 requests to the server:

.. code-block:: python

    area_alerts = nwsapy.get_all_alerts(area = ["This is where a list of all areas would go."])
    marine_alerts = nwsapy.get_all_alerts(region = ['List of marine regions'])
    n_alerts = len(area_alerts) + len(marine_alerts)

API Reference: Alert Count
--------------------------
Method: get_alert_count
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_alert_count

Class: AlertByCount
^^^^^^^^^^^^^^^^^^^
.. autoclass:: nwsapy.alerts.AlertByCount
	:members:


