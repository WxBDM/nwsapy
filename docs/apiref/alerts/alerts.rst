Alerts
======

The methods that retrieves alerts gets information from the following endpoints:

    | ``/alerts``
    | ``/alerts/active``
    | ``/alerts/types``
    | ``/alerts/{id}``
    | ``/alerts/active/count``
    | ``/alerts/active/zone/{zoneId}``
    | ``/alerts/active/area/{area}``
    | ``/alerts/active/region/{region}``

API Endpoint: Alerts
--------------------

The following table shows all alert-related NWSAPy functions are and what the equivalent API endpoint it is.

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

For example, if you would like to retrieve the alert types from ``/alerts/types``, you would call :meth:`nwsapy.get_alert_types()`. This would then return an object containing the information from the API in an :class:`alerts.AlertTypes` object. :class:`alerts.IndividualAlerts` are not returned from any of these objects. Rather, these are objects that contain information about a singular alert in the associated alert object.


Most Alert objects are...
-------------------------

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

.. toctree::
    :hidden:
    :maxdepth: 1

    All Alerts <AllAlerts>
    Active Alerts <ActiveAlerts>
    Alert Type <AlertTypes>
    Alert by Id <AlertById>
    Alert by Count <AlertByCount>
    Alert by Zone <AlertByZone>
    Alert by Area <AlertByArea>
    Alert by Marine Region <AlertByMarineRegion>
    Individual Alerts <IndividualAlerts>
    Data Validation Tables <datavalidationtables>
    Alert Errors <Error>
