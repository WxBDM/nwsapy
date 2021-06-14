===============
Getting Started
===============

Installation
------------

You can install APy through ``pip``::

	pip install nwsapy

Once it's installed, go ahead and test it with this small script:

.. code-block:: python

	from nwsapy import nwsapy
	
	nwsapy.set_user_agent("Application Name", "youremail@domain.com")
	server_ping = nwsapy.ping_server()
	print(server_ping.status)

This should give you::

	OK

Note: The NWS API does require a ``User Agent``, as this is a form of authentication. In accordance to their documentation:

"A User Agent is required to identify your application. This string can be anything, and the more unique to your application the less likely it will be affected by a security event. If you include contact information (website or email), we can contact you if your string is associated to a security event. This will be replaced with an API key in the future."

APy gives functionality so that you're able to set this field (and other kinds of header information). See https://www.weather.gov/documentation/services-web-api#/ for more information regarding the User Agent and other header fields.

Rate Limit
----------
When using this package, you may encounter the rate limit. This is a limit in which the maintainers of the API have set. If you encounter this, wait 30 seconds before trying again.

Understanding the Docs
----------------------

The API Reference is a blend of both explanations and pure reference. It's broken down into tags based off of how the NWS API is set up (i.e. ``/alerts``, ``/stations``, ``/radar``, etc), which are called ``modules`` (not to be confused with Python modules). The layout and format of this documentation follows how pandas is laid out.

The top-most page (i.e. ``Alerts``, ``Glossary``, ``Gridpoints``, etc) contains explanations on what the module does, what URL's are requested, and any "Data Validation" table. When expanded on the left side, it will show all ``nwsapy`` functions associated with the module. These functions will return an instantiated object, which the methods associated with the object are shown when expanded upon.

Data Validation
---------------

If there are any parameters for any ``nwsapy`` method, a data validation table will be provided at the top-most level of the module (i.e. ``Alerts``, ``Glossary``, etc). To simply put, data validation tables give you a way to make sure that your parameters are formatted properly to minimize 404 errors.

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



