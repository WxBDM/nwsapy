.. NWS API documentation master file, created by
   sphinx-quickstart on Wed May 12 10:35:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=====================================================================
NWSAPy: A Pythonic Implementation of the National Weather Service API
=====================================================================

NWSAPy (APy, for short) is designed to be a pythonic approach to utilizing the National Weather Service API. The goals of the package are simple:

- **Maintain clean, simplistic, minimal, and consistent user-end code**
- **Construct URLs and request data on your behalf**
- **Minimize API knowledge overhead**

Here's a few brief examples of how easy it is to use the package:

Let's say we want to get all of the tornado warnings, then package all the information together in a dataframe:

.. code-block:: python

   from nwsapy import nwsapy

   nwsapy.set_user_agent("Application Name", "youremail@domain.com or website")
   active_tor_warnings = nwsapy.get_active_alerts(event = "Tornado Warning")
   df = active_tor_warnings.to_dataframe()

Suppose we want to convert units to pint:

.. code-block:: python

   from nwsapy import nwsapy
   from pint import UnitRegistry

   nwsapy.set_user_agent("Application Name", "youremail@domain.com or website")
   point = nwsapy.get_point(32.6099, -85.4808)  # Auburn, AL
   point = point.to_pint(UnitRegistry())  # pass in your unit registry
   print(point.distance) # 854.1731315087 meter

Implementation of the full API is in progress. The documentation will update on an as-needed basis to reflect this.

The National Weather Service API can be found here: https://www.weather.gov/documentation/services-web-api#/

Table of Contents
=================
.. toctree::
   :maxdepth: 1
   
   Getting Started <gettingstarted>
   API Reference <apiref>
   Developer's Notes <dev_notes>

Advantages of using NWSAPy
==========================
- **Clean and Simplistic Code** - The syntax is very english-like.
- **No worries about JSON**. NWSAPy takes care of anything JSON-related, including formats (GeoJSON, JSON-LD, etc).
- **No worries about URLs**. Similar to the Django ORM, you're able to make a request without ever writing code to make a request.
- **404 Error Minimization.** This is handled through data validation checks, as well as handling URL construction.
- **Response errors are handled.** Response errors are handled appropriately.

Dependencies
============

NWSAPy has minimal dependencies, with core functionality being pure python:

- shapely
- pandas
- numpy
- requests
- pint

Contact
=======

It motivates me to continue support and development for this package if I hear from the community. If you have questions or comments relating to the package, you can tweet at me: @WxBDM. If a bug is identified, open an issue on GitHub. Please provide steps on how to recreate the issue with an example. If you'd like to contribute, please issue a pull request.

Important Links
===============

- `GitHub <https://github.com/WxBDM/nwsapy>`_
- `National Weather Service API Documentation <https://www.weather.gov/documentation/services-web-api>`_
- `National Weather Service API <https://api.weather.gov/>`_
- `National Weather Service API Discussion <https://github.com/weather-gov/api/discussions>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
