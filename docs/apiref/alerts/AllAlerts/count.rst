All Alerts: Count
=================

.. currentmodule:: nwsapy.alerts
.. automethod:: AllAlerts.count
	:noindex:

**Examples**


Get the number of severe thunderstorm watches AND warnings:

>>> all_alerts = nwsapy.get_all_alerts()
>>> svr_tstorm = all_alerts.count(['Severe Thunderstorm Watch', 'Severe Thunderstorm Warning'])
>>> print(f'Watches: {svr_tstorm[0]}\nWarnings: {svr_tstorm[1]}')
Watches: 9
Warnings: 11

Alternatively:

>>> all_alerts = nwsapy.get_all_alerts()
>>> watches = all_alerts.count('Severe Thunderstorm Watch')
>>> warnings = all_alerts.count('Severe Thunderstorm Warning')
>>> print(f'Watches: {watches}\nWarnings: {warnings}')
Watches: 9
Warnings: 11