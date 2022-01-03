===============
Getting Started
===============

.. currentmodule:: nwsapy.NWSAPy

Installation
------------

You can install APy through ``pip``::

	pip install nwsapy

Once it's installed, go ahead and test it with this small script:

.. code-block:: python

	from nwsapy import api_connector
	
	api_connector.set_user_agent("Application Name", "youremail@domain.com")
	server_ping = api_connector.ping_server()

	# Always a good idea to check to make sure an error didn't occur.
	# There are times when a 400 or 500 error will occur.
	if server_ping.has_any_request_errors:
	    print(f"Error from server. Details: {server_ping}")
	else:
    	print(server_ping.status)  # will print OK

This should give you::

	OK

Note: The NWS API does require a ``User Agent``, as this is a form of 
authentication. In accordance to their documentation:

	"A User Agent is required to identify your application. This string can be 
	anything, and the more unique to your application the less likely it will be 
	affected by a security event. If you include contact information 
	(website or email), we can contact you if your string is associated to a 
	security event. This will be replaced with an API key in the future."

APy gives functionality so that you're able to set this field 
(and other kinds of header information). See 
https://www.weather.gov/documentation/services-web-api#/ for more information 
regarding the User Agent and other header fields.

I want to...
------------

Get watches and warnings
^^^^^^^^^^^^^^^^^^^^^^^^
The NWS API provides a way for you to get various alerts. The table below provides 
a reference as to which methods to call using NWSAPy:

+-----------------------------------------+--------------------------------------+
| Description                             | NWSAPy Method                        |
+=========================================+======================================+
| Get all of the alerts.                  | :meth:`get_alerts()`                 |
+-----------------------------------------+--------------------------------------+
| Get the current active alerts.          | :meth:`get_active_alerts()`          |
+-----------------------------------------+--------------------------------------+
| Get all the types of alerts.            | :meth:`get_alert_types()`            |
+-----------------------------------------+--------------------------------------+
| Get active alerts by their ID.          | :meth:`get_alert_by_id()`            |
+-----------------------------------------+--------------------------------------+
| Get the number of active alerts.        | :meth:`get_alert_count()`            |
+-----------------------------------------+--------------------------------------+
| Get the active alerts by zone.          | :meth:`get_alert_by_zone()`          |
+-----------------------------------------+--------------------------------------+
| Get the active alerts by area.          | :meth:`get_alert_by_area()`          |
+-----------------------------------------+--------------------------------------+
| Get the active alerts by marine region. | :meth:`get_alert_by_marine_region()` |
+-----------------------------------------+--------------------------------------+

Get definitions of words I don't understand!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
No worries, the NWS API does provide a glossary for you: :meth:`get_glossary`.

Get metadata about a specific lat/lon point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use :meth:`get_point`.

Rate Limit
----------
When using this package, you may encounter the rate limit. 
This is a limit in which the maintainers of the API have set, but is not publicly
known. If you encounter this, wait a few seconds before trying again.

Data Validation
---------------

If there are any parameters for any ``nwsapy`` method, the parameters will be 
validated against :ref:`Data Validation Tables` listed in the documentation. 

.. important::

	If you were to use NWSAPy in an application that you plan on deploying, 
	you want to ensure that the parameters are formatted properly before calling 
	any ``nwsapy`` functions. Data Validation Errors and Parameter Type Errors
	should only appear during development and will stop your code from running.

For example, if we were run the following code:

.. code-block:: python

	from nwsapy import api_connector
	
	api_connector.set_user_agent("NWSAPy", "your_email@email.com or website")
	area_alert = api_connector.get_alert_by_area('FL')

We would retrieve all of the active alerts from Florida. However, if we were to 
attempt to run this code:

.. code-block:: python

	from nwsapy import api_connector
	
	api_connector.set_user_agent("NWSAPy", "your_email@email.com or website")
	area_alert = api_connector.get_alert_by_area('Flo-rida')

An error would be raised:

>>> area_alert = api_connector.get_alert_by_area('Flo-rida')
nwsapy.core.errors.DataValidationError: Invalid data input: '['Flo-rida']'. See documentation for valid inputs.

This is because ``Flo-rida`` isn't in the associated Data Validation Table for
this parameter.