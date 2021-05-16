API Reference
=============

The package is split into sections where individual requests to the API are grouped together. They are grouped together by the first part in the URL address (e.g. ``/products/`` or ``/zones``).

Each section below contains information about the module, what functions to call from the main NWSAPy package, what NWSAPy object is returned, and the equivalent API URL request would be.

Note that the package handles API URL requests on your behalf. Currently, you are not able to modify what these URL's look like (i.e. starting/ending times), but a future version will allow for this.

.. toctree::
   :maxdepth: 1

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