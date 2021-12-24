===============
Getting Started
===============

.. currentmodule:: nwsapy

Installation
------------

You can install APy through ``pip``::

	pip install nwsapy

Once it's installed, go ahead and test it with this small script:

.. code-block:: python

	from nwsapy import nwsapy
	
	nwsapy.set_user_agent("Application Name", "youremail@domain.com")
	server_ping = nwsapy.ping_server()

	# Always a good idea to check to make sure an error didn't occur.
	# There are times when a 400 or 500 error will occur.
	if server_ping.has_any_request_errors:
	    print(f"Error from server. Details: {server_ping}")
	else:
        print(server_ping.status)  # will print OK

This should give you::

	OK

Note: The NWS API does require a ``User Agent``, as this is a form of authentication. In accordance to their documentation:

"A User Agent is required to identify your application. This string can be anything, and the more unique to your application the less likely it will be affected by a security event. If you include contact information (website or email), we can contact you if your string is associated to a security event. This will be replaced with an API key in the future."

APy gives functionality so that you're able to set this field (and other kinds of header information). See https://www.weather.gov/documentation/services-web-api#/ for more information regarding the User Agent and other header fields.

I want to...
------------

Get watches and warnings
^^^^^^^^^^^^^^^^^^^^^^^^
The API provides a way for you to get various alerts. The table below provides a reference as to which methods to call:

+-----------------------------------------+---------------------------------------------+
| Description                             | NWSAPy Method                               |
+=========================================+=============================================+
| Get all of the alerts.                  | :meth:`nwsapy.get_all_alerts()`             |
+-----------------------------------------+---------------------------------------------+
| Get the current active alerts.          | :meth:`nwsapy.get_active_alerts()`          |
+-----------------------------------------+---------------------------------------------+
| Get all the types of alerts.            | :meth:`nwsapy.get_alert_types()`            |
+-----------------------------------------+---------------------------------------------+
| Get active alerts by their ID.          | :meth:`nwsapy.get_alert_by_id()`            |
+-----------------------------------------+---------------------------------------------+
| Get the number of active alerts.        | :meth:`nwsapy.get_alert_count()`            |
+-----------------------------------------+---------------------------------------------+
| Get the active alerts by zone.          | :meth:`nwsapy.get_alert_by_zone()`          |
+-----------------------------------------+---------------------------------------------+
| Get the active alerts by area.          | :meth:`nwsapy.get_alert_by_area()`          |
+-----------------------------------------+---------------------------------------------+
| Get the active alerts by marine region. | :meth:`nwsapy.get_alert_by_marine_region()` |
+-----------------------------------------+---------------------------------------------+

Get the forecast for a specific lat/lon
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This functionality has not been implemented directly as of v0.2.0. In a near future version, it will be implemented.

Get definitions of words I don't understand!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
No worries, the API does provide a glossary for you: :meth:`nwsapy.get_glossary()`.

Rate Limit
----------
When using this package, you may encounter the rate limit. This is a limit in which the maintainers of the API have set. If you encounter this, wait 30 seconds before trying again.

Understanding the Docs
----------------------
The API Reference is a blend of both explanations and pure reference. Each page begins with an introduction and shows a few examples on how to use the appropriate function. It also provides an explanation of the object that is returned from the function.

Data Validation
---------------

If there are any parameters for any ``nwsapy`` method, the parameters will be validated against Data Validation Tables listed in the documentation. These tables are

.. important::

	If you were to use NWSAPy in an application that you plan on deploying, you want to ensure that the parameters are formatted properly before calling any ``nwsapy`` functions. Data Validation Errors and Parameter Type Errors should only appear during development.

For example, if we were run the following code:

.. code-block:: python

	from nwsapy import nwsapy
	
	nwsapy.set_user_agent("NWSAPy", "your_email@email.com or website")
	area_alert = nwsapy.get_alert_by_area('FL')

We would retrieve all of the active alerts from Florida. However, if we were to attempt to run this code:

.. code-block:: python

	from nwsapy import nwsapy
	
	nwsapy.set_user_agent("NWSAPy", "your_email@email.com or website")
	area_alert = nwsapy.get_alert_by_area('Florida')

An error would be raised:

>>> area_alert = nwsapy.get_alert_by_area('Florida')
nwsapy.errors.DataValidationError: Invalid data input: '['Florida']'. See documentation for valid inputs.

If you were to refer to the documentation (in this case, ``Alerts`` as you're calling a method that gets all of the active alerts), ``Florida`` is not on the table.



