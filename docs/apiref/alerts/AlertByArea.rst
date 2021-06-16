Alerts by Area
==============

.. currentmodule:: nwsapy

Introduction: Alert by Area
---------------------------
To get alerts by area, use:

.. code-block:: python

    nwsapy.get_alert_by_area("AREA")

This will return an ``AlertByArea`` object, as described in the API reference below. This is equivalent to the all alerts endpoint code: ``nwsapy.get_all_alerts(area = "AREA")``.

The ``AlertByArea`` object is iterable and indexable:

.. code-block:: python

    alabama_alerts = nwsapy.get_alert_by_area("AL")

    for alert in alabama_alerts:
        print(alert.headline)

    first_alert = alabama_alerts[0]

The ``AlertByArea`` object is comprised of Individual Alert objects.

The methods that are implemented for ``AlertByArea`` are::

    to_dataframe()
    to_dict()

Example Usage: Alert by Area
----------------------------
It's a lot quicker to use this method if you are only filtering alerts by areas. The introduction section shows one way of using this method. You could also pass in a list of valid areas:

.. code-block:: python

    three_state_alerts = nwsapy.get_alert_by_area(['OK', 'AL', 'FL'])

However, it should be noted that if you are filtering by multiple areas, it would be quicker to use ``get_active_alerts`` in an instance like this.

The API does not offer additional parameters for this endpoint. So, if you need to get tornado warnings in Wyoming, you can't do:

.. code-block:: python

    this_doesnt_work = nwsapy.get_alert_by_area(region = "WY", event = "Tornado Warning")

You'll have to use ``get_active_alerts``.

API Reference: Alert by Area
----------------------------

Method: get_alert_by_area
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_alert_by_area(area)

Class: alerts.AlertByArea
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.alerts.AlertByArea( )
    :inherited-members:
    :members:
