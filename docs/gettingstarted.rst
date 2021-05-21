===============
Getting Started
===============

Installation
------------

You can install NWSAPy through ``pip``::

	pip install nwsapy

Once it's installed, go ahead and test it with this small script and replace the email field in ``set_user_agent()``:

.. code-block:: python

	from nwsapy import nwsapy
	
	nwsapy.set_user_agent("NWSAPy", "your_email@email.com")
	server_ping = nwsapy.ping_server()
	print(server_ping.status)
	

This should give you::

	OK


Note: The NWS API does require a ``User Agent``, as this is a form of authentication. NWSAPy gives funcitonality so that you're able to set this field (and other kinds of header information). See https://www.weather.gov/documentation/services-web-api#/ for more information.

Understanding the Docs
----------------------

The API Reference is a blend of both explainations and pure reference. It's broken down into tags based off of how the NWS API is set up (i.e. ``/alerts``, ``/stations``, ``/radar``, etc), which are called ``modules`` (not to be confused with Python modules). The layout and format of this documentation follows how pandas is laid out. 

The top-most page (i.e. ``Alerts``, ``Glossary``, ``Gridpoints``, etc) contains explainations on what the module does, what URL's are requested, and any "Data Validation" table. When expanded on the left side, it will show all ``nwsapy`` functions associated with the module. These functions will return an instantiated object, which the methods associated with the object are shown when expanded upon.

Data Validation
---------------

If there are any parameters for any ``nwsapy`` method, a data validation table will be provided at the top-most level of the module (i.e. ``Alerts``, ``Glossary``, etc). To simply put, data validation tables give you a way to make sure that your parameters are formatted properly to minimize 404 errors.

.. important::

	If you were to use NWSAPy in an application that you plan on deploying, you want to ensure that the parameters are formatted properly before calling any ``nwsapy`` functions. Data Validation Errors and Parameter Type Errors should only appear during development.

For example, if we were run the following code:

.. code-block:: python

	from nwsapy import nwsapy
	
	nwsapy.set_user_agent("NWSAPy", "your_email@email.com")
	area_alert = nwsapy.get_alert_by_area('FL')

We would retrieve all of the active alerts from Florida. However, if we were to attempt to run this code:

.. code-block:: python

	from nwsapy import nwsapy
	
	nwsapy.set_user_agent("NWSAPy", "your_email@email.com")
	area_alert = nwsapy.get_alert_by_area('Florida')

An error would be raised:

>>> area_alert = nwsapy.get_alert_by_area('Florida')
nwsapy.errors.DataValidationError: Invalid data input: '['Florida']'. See documentation for valid inputs

If you were to refer to the documentation (in this case, ``Alerts`` as you're calling a method that gets all of the active alerts), ``Florida`` is not on the table.

.. toctree::
    :maxdepth: 1
    :hidden:
	
    Alerts <apiref/alerts/alerts>
    Glossary <apiref/glossary>
    Gridpoints <apiref/gridpoints>
    Icons <apiref/icons>
    Thumbnail <apiref/thumbnails>
    Stations <apiref/stations>
    Offices <apiref/offices>
    Points <apiref/points>
    Radar <apiref/radar>
    Products <apiref/products>
    Zones <apiref/zones>



