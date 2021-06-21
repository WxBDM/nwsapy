Developer's Notes
=================

This is a collection of my thoughts and notes while developing this package of things to keep in mind while developing using APy. These are not in any particular order. This page is not maintained on a regular basis.

Requesting
----------
Be nice to their servers, use minimal requesting. Most ``get()`` methods are 1 request, but there are some exceptions:

    | ``get_alert_by_area()``
    | ``get_alert_by_zone()``
    | ``get_alert_by_id()``
    | ``get_alert_by_marine_region()``

These methods will request for every element in the list that is passed in. For example: ``get_alert_by_area(["OH", "PA"])`` will request twice.

Getting Forecasts
-----------------
When the ``gridpoints`` endpoints gets implemented, there shouldn't be a ``get_forecast()`` method. This is because you want to ideally put together a database or cache for gridpoints. To get a forecast, you have to request twice: once to get the associated grid for that point and another to get the forecast itself.

Some driver code pairing it against a database (without associated methods written):

.. code-block:: python

    lat = 30
    lon = -90

    # Check to see if this specific lat/lon is in the database.
    is_in_db = is_point_in_db(lat, lon)

    if is_in_db.exists: # This is ideal! If it is, get the forecast (1 request)
        forecast = nwsapy.get_gridpoint(is_in_db.cwa, is_in_db.lat, is_in_db.lon)
    else: # If not, get the point, then get the forecast.
        point = nwsapy.get_point(lat, lon)
        forecast = nwsapy.get_gridpoint(point.cwa, (point.gridX, point.gridY))

You can also do the same thing with an in-memory cache.

Benchmark Testing: Alerts
-------------------------
I've performed some benchmark tests to see what would be the most optimal for alerts. This specific benchmark test occurred on Sunday, June 2021. During the benchmark test, the NWS watches, warnings, and advisory map was as such:

.. image:: docs/_static/US.png

Thus, any alerts in states such as Nebraska, SD, or ND would be skewed in terms of time, as there are minimal watches/warnings there.

The benchmark was purely empirical. That is, a timer was used to determine the time it took to compare 3 alert methods: ``get_all_alerts()``, ``get_alert_by_area()``, and ``get_active_alerts()``.

.. code-block:: python

                 all     active       area
    count  10.000000  10.000000  10.000000
    mean    2.122451   1.440446   1.284262
    std     1.202978   0.709636   0.764525
    min     0.747752   0.580143   0.523200
    25%     1.148271   0.915316   0.770044
    50%     1.678807   1.267500   1.113227
    75%     3.010713   1.929299   1.588442
    max     3.915961   2.834346   3.087599
