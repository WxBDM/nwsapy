Modules
=======

The package is split into modules (not to be confused with the Python modules), where individual requests to the API are grouped together. They are grouped together by the first part in the URL address (e.g. ``/products/`` or ``/zones``).

Each section below contains information about the module, what functions to call from the main NWSAPy package, what NWSAPy object is returned, and the equivalent API URL request would be.

Note that the package handles API URL requests on your behalf. Currently, you are not able to modify what these URL's look like (i.e. starting/ending times), but a future version will allow for this.

.. toctree::
   :maxdepth: 2

   Alerts <alerts>
   Glossary <glossary>
   Gridpoints <gridpoints>
   Icons <icons>
   Thumbnail <thumbnails>
   Stations <stations>
   Offices <offices>
   Points <points>
   Radar <radar>
   Products <products>
   Zones <zones>