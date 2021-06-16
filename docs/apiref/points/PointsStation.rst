Point Station
==============

.. currentmodule:: nwsapy

Introduction: Point Station
---------------------------
The point station method retrieves a list of observation stations for a given point. To use:

.. code-block:: python

    nwsapy.get_point_station(lat, lon)

This will return an ``PointStation`` object, as described in the API reference below.

The ``PointStation`` object is iterable and indexable, comprising of ``Station`` objects:

.. code-block:: python

    auburn = nwsapy.get_point_station(32.6099, -85.4808)

    for station_near_auburn in auburn:
        print(station_near_auburn.name)

    first_station_near_auburn = auburn[0]

The methods that are implemented for :class:`PointStation` are::

    to_dict()
    to_dataframe()
    to_pint()

It should be noted that the lat/lon is rounded to the closest 4 decimal places. This limitation is imposed by the API.

Example Usage: Point Station
----------------------------
As of v0.2.0, you can only read in floats and integers. In a future version, you'll be able to read in a shapely point. But for now:

.. code-block:: python

    auburn = nwsapy.get_point_station(32.6099, -85.4808)

You can also read in a lat/lon more than 4 decimals, but it will be rounded to the nearest 4th decimal:

.. code-block:: python

    auburn = nwsapy.get_point_station(32.609900001, -85.480800001)
    # This will round to 32.6099, -85.4808

API Reference: Point Station
----------------------------

Method: get_point_station
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_point_station(lat, lon)

Class: points.PointStation
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.points.PointStation( )
    :inherited-members:
    :members: