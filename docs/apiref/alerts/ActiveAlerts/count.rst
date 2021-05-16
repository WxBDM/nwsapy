Active Alerts: Count
====================

.. automethod:: alerts.ActiveAlerts.count
	:noindex:

**Examples**

Get the number of severe thunderstorm watches AND warnings:

>>> all_alerts = nwsapy.get_active_alerts()
>>> svr_tstorm = all_alerts.count(['Severe Thunderstorm Watch', 'Severe Thunderstorm Warning'])
>>> print(f'Watches: {svr_tstorm[0]}\nWarnings: {svr_tstorm[1]}')
Watches: 12
Warnings: 17

Alternatively:

>>> all_alerts = nwsapy.get_active_alerts()
>>> watches = all_alerts.count('Severe Thunderstorm Watch')
>>> warnings = all_alerts.count('Severe Thunderstorm Warning')
>>> print(f'Watches: {watches}\nWarnings: {warnings}')
Watches: 12
Warnings: 17