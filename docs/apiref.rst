API Reference
=============

.. currentmodule:: nwsapy

The API reference is really a blend between examples and an API reference. The API reference is split up based upon which endpoint it is referencing. Each page has an overview of what the endpoint is, provides some basic examples on how to get started with it, then provides the associated :class:`NWSAPy` method, as well as the object that it returns.

Since errors (such as 404 or 500) are handled by creating an error object, you may want to check to see if the error object exists. NWSAPy allows you to easily check:

.. code-block:: python

    alerts = nwsapy.get_all_alerts()

    # Check if there's any errors
    if alerts.has_any_request_errors:
        error_obj = alerts[0] # error obj is stored in the list.
        raise Error(f"Alerts an error object. Code: {error_obj.code}")
        # or however else you want to handle the error.

    # continue doing what you were doing with your application.

Table of Contents: Endpoints
----------------------------

.. toctree::
   :maxdepth: 1

   Alerts <apiref/alerts/alerts>
   Glossary <apiref/glossary>
   Gridpoints <apiref/gridpoints>
   Icons <apiref/icons>
   Thumbnail <apiref/thumbnails>
   Stations <apiref/stations>
   Offices <apiref/offices>
   Points <apiref/points/points>
   Radar <apiref/radar>
   Products <apiref/products>
   Zones <apiref/zones>

NWSAPy Methods
--------------

.. currentmodule:: nwsapy
.. autoclass:: nwsapy.NWSAPy
    :noindex:
    :members:
