Alerts by ID: Count
===================

.. currentmodule:: nwsapy.alerts
.. automethod:: AllAlerts.count
	:noindex:

**Examples**

>>> all_alerts = nwsapy.get_alert_by_id(['urn:oid:2.49.0.1.840.0.050e935e72efe1d507886e3b5e8ddc619f494f6a.001.1',
                                    'urn:oid:2.49.0.1.840.0.8a1ffcf23f9b0f16ae92d256fe23ed01c239278b.001.1'])
>>> svr_tstorm = all_alerts.count(['Severe Thunderstorm Watch', 'Severe Thunderstorm Warning'])
>>> print(f'Watches: {svr_tstorm[0]}\nWarnings: {svr_tstorm[1]})
Watches: 0
Warnings: 1

Alternatively:

>>> all_alerts = nwsapy.get_alert_by_id(['urn:oid:2.49.0.1.840.0.050e935e72efe1d507886e3b5e8ddc619f494f6a.001.1',
                                   'urn:oid:2.49.0.1.840.0.8a1ffcf23f9b0f16ae92d256fe23ed01c239278b.001.1'])
>>> watches = all_alerts.count('Severe Thunderstorm Watch')
>>> warnings = all_alerts.count('Severe Thunderstorm Warning')
>>> print(f'Watches: {watches}\nWarnings: {warnings}')
Watches: 0
Warnings: 1