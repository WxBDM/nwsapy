.. NWS API documentation master file, created by
   sphinx-quickstart on Wed May 12 10:35:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================================
NWSAPy: An Object Oriented Approach to the NWS API
==================================================

NWSAPy (APy, for short) is designed to streamline the process of retrieving information from the National Weather Service API. It fetches (GET) then organizes the data in an object-oriented manner. For example, if we wanted to show the headline for all of the current severe thunderstorm warnings:

.. code-block:: python

	from nwsapy import nwsapy

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
- **Clean and Simplistic Code** - The syntax is very english-like.
- **No worries about JSON**. NWSAPy takes care of anything JSON-related, including formats (GeoJSON, JSON-LD, etc).
- **No worries about URLs**. NWSAPy also takes care of handling request URL's
- **404 Error Minimization.** This is handled through data validation checks, as well as handling URL construction.
- **Response errors are handled.** Response errors are handled appropriately.
- **Consistency matters.** Even if the response doesn't have a specific attribute, NWSAPy makes sure *something* exists so your code doesn't break.

Dependencies
============

NWSAPy has minimal dependecies:

- shapely
- pandas
- numpy
- requests

Contact
=======

It motivates me to continue support for this package if I hear from the community. If you have questions or comments relating to the package, you can email me at brandonmolyneaux@torandotalk.com. If a bug is identified, open an issue on GitHub.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
