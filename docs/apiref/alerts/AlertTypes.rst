Alert Types
===========

.. currentmodule:: nwsapy

Introduction: Alert Types
-------------------------
To get alert types, use:

.. code-block:: python

    nwsapy.get_alert_types()

This will return an ``AlertTypes`` object, as described in the API reference below.

The ``AlertTypes`` object is iterable and indexable:

.. code-block:: python

    washington_dc = nwsapy.get_alert_types()

    for alert in washington_dc:
        print(alert.headline)

    first_alert = washington_dc[0]

The ``AlertTypes`` object is comprised of Individual Alert objects.

There are no methods implemented for this object.

API Reference: Alert Types
--------------------------

Method: get_alert_types
^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_alert_types()

Class: alerts.AlertTypes
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: nwsapy.alerts.AlertTypes( )
    :inherited-members:
    :members:
