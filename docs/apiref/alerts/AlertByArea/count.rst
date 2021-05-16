Alert by Area: Count
====================

.. automethod:: alerts.AlertByArea.count
	:noindex:

**Examples**


Get the number of severe thunderstorm watches and warnings, as well as tornado watches and warnings:

>>> all_alerts = nwsapy.get_alert_by_area('NE')
>>> counted = all_alerts.count(['Severe Thunderstorm Watch', 'Severe Thunderstorm Warning', 'Tornado Watch', 'Tornado Warning'])
>>> print(f'Severe Tstorm Watches: {counted[0]}\nSevere Tstorm Warnings: {counted[1]}\nTornado Watches: {counted[2]}\nTornado Warnings: {counted[3]}')
Severe Tstorm Watches: 0
Severe Tstorm Warnings: 1
Tornado Watches: 0
Tornado Warnings: 0

Alternatively:

>>> all_alerts = nwsapy.get_all_alerts()
>>> tstorm_watch = all_alerts.count('Severe Thunderstorm Watch')
>>> tstorm_warn = all_alerts.count('Severe Thunderstorm Warning')
>>> tor_watch = all_alerts.count('Tornado watch')
>>> tor_warning = all_alerts.count('Tornado Warning')
>>> print(f'Severe Tstorm Watches: {tstorm_watch}\nSevere Tstorm Warnings: {tstorm_warn}\nTornado Watches: {tor_watch}\nTornado Warnings: {tor_warning}')
Severe Tstorm Watches: 0
Severe Tstorm Warnings: 1
Tornado Watches: 0
Tornado Warnings: 0