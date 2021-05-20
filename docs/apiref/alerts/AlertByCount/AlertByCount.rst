Alert Count
===========

.. currentmodule:: nwsapy
.. automethod:: nwsapy.get_alert_count

|

.. note:: If there is not an error (404, 500, etc) then ``.alerts`` will be ``None``. All other attributes will have values. If there is an error, then ``.alerts`` will contain an Individual Alert Errror and all other attributes will be ``None``.


.. autoclass:: nwsapy.alerts.AlertByCount
	:members:

	.. note:: This does not contain the dynamically created alert objects, as it only contains a count of the active alerts.

.. toctree::
	:maxdepth: 1
	:hidden:
	
	alerts.AlertByCount.filter_land_areas <filter_land_areas>
	alerts.AlertByCount.filter_marine_regions <filter_marine_regions>
	alerts.AlertByCount.filter_zones <filter_zones>

