Point Error
===========

Introduction: Point Error
-------------------------
One of the biggest advantages of NWSAPy is that it is designed to reduce the number of errors. Namely, 404 errors regarding URL construction, as well as parameter data type/structure. As such, you shouldn't see error objects on a regular basis. However, they are possible to get due to rate limit or request time out.

For reference, the link for a description of the HTTP errors are here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

Example: Point Error
--------------------
In your application, you may want to check to see if you have any request errors. APy allows you to easily see if you do or not:

.. code-block:: python

    # make a request for alerts
    alerts = nwsapy.get_point(20, -90)

    # check to see if there were any errors.
    if alerts.has_any_request_errors:
        print("There was a request error!")
        # Handle this however your application handles errors.

It should be noted that the ``Point`` object will have at most 1 error. ``PointsStation`` objects can not have an error object, as they do not make requests. All other alert objects can have at least 1 error object.

You can peek at the number of errors as well:

.. code-block:: python

    stations = nwsapy.get_point_station(20, -90)

    if stations.has_any_request_errors:
        print(stations.n_errors) # shows the number of station errors

API Reference: Point Error
--------------------------

.. autoclass:: nwsapy.points.PointError( )
    :members: