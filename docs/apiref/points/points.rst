Points
======

The methods that retrieves points gets information from the following endpoints:

    | ``/points/{point}``
    | ``/points/{point}/stations``

API Endpoint: Point
-------------------

The following table shows all point-related NWSAPy functions are and what the equivalent API endpoint it is.

.. py:currentmodule:: nwsapy

+------------------------------------+-----------------------------+-------------------------------------------------------------------+
| NWSAPy Method                      | Associated Point Object     | Description                                                       |
+====================================+=============================+===================================================================+
| :meth:`nwsapy.get_point()`         | :class:`point.Point`        | Retrieves information about a given point.                        |
+------------------------------------+-----------------------------+-------------------------------------------------------------------+
| :meth:`nwsapy.get_point_station()` | :class:`point.PointStation` | Retrieves information about observation stations near this point. |
+------------------------------------+-----------------------------+-------------------------------------------------------------------+

.. toctree::
    :hidden:
    :maxdepth: 1

    Point <Point>
    Point Station <PointsStation>
    Point Errors <Error>
    Stations <Station>

