Alerts by ID
============

.. currentmodule:: nwsapy

Introduction: Alert by ID
-------------------------
To get alerts by ID, use:

.. code-block:: python

    nwsapy.get_alert_by_id("ID")

This will return an ``AlertByID`` object, as described in the API reference below.

The ``AlertByID`` object is iterable and indexable:

.. code-block:: python

    alert_id = nwsapy.get_alert_by_id("urn:oid:2.49.0.1.840.0.069714a0e67bc53c6a0330508584c3f1f5474b61.004.1")

    for alert in alert_id:
        print(alert.headline)

    first_alert = alert_id[0]

The ``AlertByID`` object is comprised of Individual Alert objects.

The methods that are implemented for :class:`AlertById` are::

    to_dataframe()
    to_dict()

Example Usage: Alert by ID
--------------------------
It's a lot quicker to use this method if you are only filtering alerts by areas. The introduction section shows one way of using this method. You could also pass in a list of valid areas:

.. code-block:: python

    three_state_alerts = nwsapy.get_alert_by_area(['List', 'of', 'all', 'the', 'ids'])

The API does not offer additional parameters for this endpoint. So, if you are looking to use this method, you should know the ID of the specific alert that you want.

.. caution::
    You are able to get 404 errors with this due to invalid data. There are no data validation checks associated with this method. There is also no parser available to ensure that the ID is structured properly.

API Reference: Alert by ID
--------------------------

Method: get_alert_by_id
^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_alert_by_id(id)

Class: alerts.AlertById
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.alerts.AlertById( )
    :inherited-members:
    :members:

