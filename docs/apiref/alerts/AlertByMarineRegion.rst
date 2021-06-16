Alerts by Marine Region
=======================

.. currentmodule:: nwsapy

Introduction: Alert by Marine Region
------------------------------------
To get alerts by marine region, use:

.. code-block:: python

    nwsapy.get_alert_by_marine_region("REGION")

This will return an ``AlertByMarineRegion`` object, as described in the API reference below. This is equivalent to the all alerts endpoint code: ``nwsapy.get_all_alerts(region = "REGION")``.

The ``AlertByMarineRegion`` object is iterable and indexable:

.. code-block:: python

    atlantic_alerts = nwsapy.get_alert_by_marine_region("AL")

    for alert in atlantic_alerts:
        print(alert.headline)

    first_alert = atlantic_alerts[0]

The ``AlertByMarineRegion`` object is comprised of Individual Alert objects.

The methods that are implemented for :class:`AlertByMarineRegion` are::

    to_dataframe()
    to_dict()

Example Usage: Alert By Marine Region
-------------------------------------
It's a lot quicker to use this method if you are only filtering alerts by marine regions. The introduction section shows one way of using this method. You could also pass in a list of valid areas:

.. code-block:: python

    three_marine_alerts = nwsapy.get_alert_by_marine_region(['PA', 'AL', 'GM'])

However, it should be noted that if you are filtering by multiple marine regions, it would be quicker to use ``get_active_alerts`` in an instance like this.

The API does not offer additional parameters for this endpoint. So, if you need to get small craft warnings in the Atlantic region, you can't do:

.. code-block:: python

    this_doesnt_work = nwsapy.get_alert_by_marine_region(region = "AL", event = "Small Craft Advisory")

You'll have to use ``get_active_alerts``.

API Reference: Alert by Marine Region
-------------------------------------

Method: get_alert_by_marine_region
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_alert_by_marine_region(region)

Class: alerts.AlertByMarineRegion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.alerts.AlertByMarineRegion
    :inherited-members:
    :members:
