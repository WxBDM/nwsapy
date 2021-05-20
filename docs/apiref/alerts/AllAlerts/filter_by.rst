All Alerts: Filter By
=====================

.. currentmodule:: nwsapy.alerts
.. automethod:: AllAlerts.filter_by
	:noindex:

**Examples**

A simple example stating the number of warnings:

>>> all_alerts = nwsapy.get_all_alerts()
>>> filtered = all_alerts.filter_by("flood warning")
>>> print(f'There are {len(filtered)} flood warnings active.')
There are 56 flood warnings active.

If we wanted to print all of the headlines, but there's additional alerts that are being filtered:

>>> all_alerts = nwsapy.get_all_alerts()
>>> filtered = all_alerts.filter_by(['Tornado Warning', 'Flash Flood Warning', 'Small Craft Advisory'])
>>> sca_advisory = [x.headline for x in filtered if isinstance(x, alerts.smallcraftadvisory)]
>>> print("Headlines for all small craft advisories:")
>>> for advisory in sca_advisory:
>>>    print(f"\t{advisory}")
Headlines for all small craft advisories:
	Small Craft Advisory issued May 15 at 2:25PM PDT until May 16 at 6:00AM PDT by NWS Eureka CA
	Small Craft Advisory issued May 15 at 2:17PM PDT until May 16 at 11:00PM PDT by NWS Portland OR

We could also isolate each individual warning type so that ``isinstance()`` isn't used:

>>> all_alerts = nwsapy.get_active_alerts()
>>> sca = all_alerts.filter_by('Small Craft Advisory')
>>> tors = all_alerts.filter_by('Tornado Warning')
>>> svr_tstorms = all_alerts.filter_by('Severe Thunderstorm Warning')

