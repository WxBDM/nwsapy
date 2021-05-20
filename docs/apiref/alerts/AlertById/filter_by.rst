Alerts by ID: Filter By
=======================

.. currentmodule:: nwsapy.alerts
.. automethod:: AlertById.filter_by
	:noindex:

**Examples**

A simple example stating the number of warnings:

>>> all_alerts = nwsapy.get_alert_by_id(['urn:oid:2.49.0.1.840.0.050e935e72efe1d507886e3b5e8ddc619f494f6a.001.1',
                                    'urn:oid:2.49.0.1.840.0.8a1ffcf23f9b0f16ae92d256fe23ed01c239278b.001.1'])
>>> svr_tstorms = all_alerts.filter_by("Severe Thunderstorm Warning")
>>> for storm in svr_tstorms:
>>> 	print(storm.headline)
Severe Thunderstorm Warning issued May 15 at 6:06PM MDT until May 15 at 6:30PM MDT by NWS Albuquerque NM

We could also isolate each individual warning type:

>>> all_alerts = nwsapy.get_alert_by_id(['urn:oid:2.49.0.1.840.0.050e935e72efe1d507886e3b5e8ddc619f494f6a.001.1',
                                    'urn:oid:2.49.0.1.840.0.8a1ffcf23f9b0f16ae92d256fe23ed01c239278b.001.1'])
>>> svr_tstorms = all_alerts.filter_by("Severe Thunderstorm Warning")
>>> print(svr_tstorms[0].headline)
Severe Thunderstorm Warning issued May 15 at 6:06PM MDT until May 15 at 6:30PM MDT by NWS Albuquerque NM

>>> special_wx_statement = all_alerts.filter_by("Special Weather Statement")
>>> print(special_wx_statement[0].headline)
Special Weather Statement issued May 15 at 5:43PM MDT by NWS Albuquerque NM


