.. NWS API documentation master file, created by
   sphinx-quickstart on Wed May 12 10:35:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============================================================
NWSAPy: A Pythonic Way to Use the National Weather Service API
==============================================================

NWSAPy (APy, for short) is designed to be a pythonic approach to utilizing the National Weather Service API. The goals of the package are simple:

- **Keep Clean, Simplistic, Minimal, and Consistent Code**
- **Minimize 404 Errors**
- **Minimize Overhead for Prerequisite API Knowledge**

Here's a few brief examples of how easy it is to use the package:

Let's say we want to put all severe thunderstorm warning information (headline, warning experation time, etc) in a pandas dataframe:

.. code-block:: python

	from nwsapy import nwsapy

	active_alerts = nwsapy.get_active_alerts()
	tstorms = active_alerts.filter_by("Severe Thunderstorm Warning")
	df = tstorms.to_dataframe()

	
Suppose you wanted to get the forecast for a specific point and display the min and max temperatures for Day 1:

.. code-block:: python

	from nwsapy import nwsapy
	
	# Forecast for Auburn, AL
	forecast = nwsapy.get_forecast_for_point(32.6099, -85.4808)
	print(forecast.day1.temp_max)
	print(forecast.day1.temp_min)
	
Implementation of the full API is in progress. The documentation will update on an as-needed basis to reflect this.

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

NWSAPy has minimal dependecies, with core functionality being pure python:

- shapely
- pandas
- numpy
- requests
- pint

Contact
=======

It motivates me to continue support for this package if I hear from the community. If you have questions or comments relating to the package, you can email me at brandonmolyneaux@torandotalk.com. If a bug is identified, open an issue on GitHub.

Important Links
===============

- `GitHub <https://github.com/WxBDM/nwsapy>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
