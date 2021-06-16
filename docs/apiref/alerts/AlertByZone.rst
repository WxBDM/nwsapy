Alerts by Zone
==============

.. currentmodule:: nwsapy

Introduction: Alert by Zone
---------------------------
To get alerts by zone, use:

.. code-block:: python

    nwsapy.get_alert_by_zone("ZONE")

This will return an ``AlertByZone`` object, as described in the API reference below. This is equivalent to the all alerts endpoint code: ``nwsapy.get_all_alerts(zone = "ZONE")``.

The ``AlertByZone`` object is iterable and indexable:

.. code-block:: python

    washington_dc = nwsapy.get_alert_by_zone("DCZ001")

    for alert in washington_dc:
        print(alert.headline)

    first_alert = washington_dc[0]

The ``AlertByZone`` object is comprised of Individual Alert objects.

The methods that are implemented for ``AlertByZone`` are::

    to_dataframe()
    to_dict()

Example Usage: Alert by Zone
----------------------------
The introduction section shows one way of using this method. You could also pass in a list of valid areas:

.. code-block:: python

    ids = ["MSC089", "MSC163"]
    three_state_alerts = nwsapy.get_alert_by_zone(ids)

However, it should be noted that if you are filtering by multiple areas, it would be quicker to use ``get_alert_by_zone`` in an instance like this.

The API does not offer additional parameters for this endpoint. So, if you need to get tornado warnings in Wyoming, you can't do:

.. code-block:: python

    this_doesnt_work = nwsapy.get_alert_by_zone(region = "MSC089", event = "Tornado Warning")

You'll have to use ``get_active_alerts``.

API Reference: Alert by Zone
----------------------------

Method: get_alert_by_zone
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_alert_by_zone(zone)

Class: alerts.AlertByZone
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.alerts.AlertByZone( )
    :inherited-members:
    :members:
