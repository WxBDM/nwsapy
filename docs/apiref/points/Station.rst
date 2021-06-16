Station
=======

.. currentmodule::nwsapy.alerts

Introduction: Station
---------------------

Stations comprise of the ``PointsStation`` class. You can retrieve the stations as such:

.. code-block:: python

        stations = nwsapy.get_point_station(32.6099, -85.4808)
        first_station = stations[0]

This will get us the first severe thunderstorm warning with that criteria:
    >>> print(first_station.city)
    https://api.weather.gov/zones/county/ALC081

Station objects themselves are not iterable nor indexable. These objects are generally used for their attributes (see API reference).

Station API Reference
---------------------

.. autoclass:: nwsapy.points.Station( )
    :members:


