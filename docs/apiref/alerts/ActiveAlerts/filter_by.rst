Active Alerts: Filter By
========================

.. currentmodule:: nwsapy.alerts

**What this method does**: Filters alerts by the given parameters.

**What this method returns**: :class:`alerts.ActiveAlerts` (itself)

**How many requests does this method make to the NWS API?** None.

**Example Usage**:

.. code-block:: python

	all_alerts = nwsapy.get_active_alerts()
	filtered = all_alerts.filter_by(event = 'Tornado Warning')

Will filter all of the alerts in the active alerts object by tornado warnings. Likewise:

.. code-block:: python

	all_alerts = nwsapy.get_active_alerts()
	filtered = all_alerts.filter_by(event = ['Tornado Warning', 'Severe Thunderstorm Warning'])
	
Will filter all of the alerts in the active alerts object to be severe thunderstorm warnings and tornado warnings.

You can also supply multiple filters: 

.. code-block:: python

	all_alerts = nwsapy.get_active_alerts()
	filtered = all_alerts.filter_by(event=["Severe Thunderstorm Warning", 'Tornado Warning'], severity='Severe')

This will filter all active alerts by the severity ranking of severe and if it's either a severe thunderstorm warning.

.. important::
	
	This will not return severe thunderstorm and tornado warnings that are of severity 'severe'. This will include all non-tornado and non-severe thunderstorm warnings that have the severity level set to be severe. To get severe thunderstorm warnings and tornado warnings based off of the "severe" severity level, you will have to call the method twice:
	
	>>> all_alerts = nwsapy.get_active_alerts()
	>>> filtered = all_alerts.filter_by(event=["Severe Thunderstorm Warning", 'Tornado Warning'])
	>>> filtered = all_alerts.filter_by(severity='Severe')
	
|

.. automethod:: ActiveAlerts.filter_by
	:noindex:

