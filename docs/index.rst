.. NWS API documentation master file, created by
   sphinx-quickstart on Wed May 12 10:35:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================================
NWSAPy: An Object Oriented Approach to the NWS API
==================================================

NWSAPy is designed to streamline the process of retreiving information from the National Weather Service API. It fetches (GET) then organizes the data in an object-oriented manner. For example, if we wanted to show the headline for all of the current severe thunderstorm warnings:

.. code-block:: python

	import nwsapy

	active_alerts = nwsapy.get_active_alerts()
	tstorms = active_alerts.filter_by("Severe Thunderstorm Warning")
	for storm in tstorms:
		print(storm.headline)

	
Will print::

> Severe Thunderstorm Warning issued May 12 at 2:50PM EDT until May 12 at 3:45PM EDT by NWS Jacksonville FL
> Severe Thunderstorm Warning issued May 12 at 2:44PM EDT until May 12 at 3:45PM EDT by NWS Jacksonville FL

The National Weather Service API can be found here: https://www.weather.gov/documentation/services-web-api#/

Table of Contents
=================
.. toctree::
   :maxdepth: 1
   
   Getting Started <gettingstarted>
   Examples <examples>
   API Reference <apiref>

Advantages of using NWSAPy
==========================
- Data validation checks: your data going in is going to be valid to minimize 404 errors.
- Response error handling is taken care of (i.e. 404, 500, etc)
- Nearly pure python code
- Minimal hassle with having to worry if links are formatted correctly.
- Clean and simplistic code
- Responses are formatted in an object oriented manner, ready to go.
- No worries about formats (GeoJSON, JSON-LD, etc). NWSAPy takes care of it for you.

Goals of the Package
====================

There are 2 goals to the package:
1. Simplify data retrieval and organization. It takes JSON structured data and converts it into something that's more object-oriented.
2. One request, one result.

Contact
=======

It motivates me to continue support for this package if I hear from the community. If you have questions or comments relating to the package, you can email me at brandonmolyneaux@torandotalk.com. If a bug is identified, open an issue on GitHub.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
