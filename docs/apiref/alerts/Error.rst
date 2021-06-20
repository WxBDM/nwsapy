Alert Error
===========

Introduction: Alert Error
-------------------------
One of the biggest advantages of NWSAPy is that it is designed to reduce the number of errors. Namely, 404 errors regarding URL construction, as well as parameter data type/structure. As such, you shouldn't see error objects on a regular basis. However, they are possible to get due to rate limit or request time out.

For reference, the link for a description of the HTTP errors are here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

Example: Alert Error
--------------------
In your application, you may want to check to see if you have any request errors. APy allows you to easily see if you do or not:

.. code-block:: python

    # make a request for alerts
    alerts = nwsapy.get_alert_by_area("WA")

    # check to see if there were any errors.
    if alerts.has_any_request_errors:
        print("There was a request error")
        # Handle this however your application handles errors.

It should be noted that ``ActiveAlerts``, ``AllAlerts``, ``AlertTypes``, and ``AlertByCount`` will only have 1 error at most per ``get()`` method. ``IndividualAlert`` objects can not have an error object, as they do not make requests. All other alert objects can have at least 1 error object.

You can peek at the number of errors as well:

.. code-block:: python

    alerts = nwsapy.get_alert_by_area(["WA", "VA", "LA"])

    if alerts.has_any_request_errors:
        print(alerts.n_errors) # shows the number of alerts

API Reference: Alert Error
--------------------------

.. autoclass:: nwsapy.alerts.AlertError( )
    :members: