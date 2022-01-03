Alert Endpoint Reference
========================

.. currentmodule:: nwsapy.endpoints.alerts

Alerts
------

Every ``Alert`` object contains at least 3 methods:

- ``to_df``
- ``to_dict``
- ``to_pint``

If the method is not implemented (that is, nothing happens when you call it),
it will be explicitly marked as "Not implmented for this endpoint".

Most of the ``Alert`` objects contain :class:`IndividualAlert` objects, which
is documented below this section.

.. autoclass:: Alerts
    :members:
    :inherited-members:

.. autoclass:: ActiveAlerts
    :members:
    :inherited-members:

.. autoclass:: AlertById
    :members:
    :inherited-members:

.. autoclass:: AlertByArea
    :members:
    :inherited-members:

.. autoclass:: AlertByZone
    :members:
    :inherited-members:

.. autoclass:: AlertByMarineRegion
    :members:
    :inherited-members:

.. autoclass:: AlertByType
    :members:
    :inherited-members:

.. autoclass:: AlertCount
    :members:
    :inherited-members:

Individual Alerts
-----------------

Individual Alert objects are the backbone to most ``Alert`` objects. Each
indivieual Alert object contains attributes.

.. currentmodule:: nwsapy

.. autoclass:: nwsapy.endpoints.alerts.IndividualAlert
    :members: