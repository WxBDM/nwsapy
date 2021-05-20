Alert by Marine Region:  Count
==============================

.. currentmodule:: nwsapy.alerts
.. automethod:: AlertByMarineRegion.count
	:noindex:

**Examples**


Get the number of small craft advisories and gale warnings for the Atlantic Ocean:

>>> all_alerts = nwsapy.get_alert_by_marine_region('AL')
>>> alerts = all_alerts.count(['Small Craft Advisory', 'Gale Warning'])
>>> print(f'Small Craft Advisories: {alerts[0]}\Gale Warnings: {alerts[1]})
Small Craft Advisories: 20
Gale Warnings: 0

Alternatively:

>>> all_alerts = nwsapy.get_all_alerts()
>>> sca = all_alerts.count('Small Craft Advisory')
>>> gw = all_alerts.count('Gale Warning')
>>> print(f'Small Craft Advisories: {sca}\Gale Warnings: {gw}')
Small Craft Advisories: 20
Gale Warnings: 0