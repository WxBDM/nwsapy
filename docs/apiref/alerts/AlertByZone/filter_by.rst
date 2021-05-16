Alert by Marine Region: Filter By
=================================

.. automethod:: alerts.AlertByMarineRegion.filter_by
	:noindex:

**Examples**

A simple example stating the number of warnings:

>>> all_alerts = nwsapy.get_alert_by_marine_region('PA')
>>> filtered = all_alerts.filter_by("small craft advisories")
>>> print(f'There are {len(filtered)} small craft advisories active.')
There are 13 small craft advisories active.

If we wanted to print all of the headlines, but there's additional alerts that are being filtered:

>>> all_alerts = nwsapy.get_alert_by_marine_region()
>>> filtered = all_alerts.filter_by(['Hazardous Seas Warning', 'Gale Warning', 'Small Craft Advisory'])
>>> sca_advisory = [x.headline for x in filtered if isinstance(x, alerts.smallcraftadvisory)]
>>> print("Headlines for all small craft advisories:")
>>> for advisory in sca_advisory:
>>>    print(f"\t{advisory}")
Headlines for all small craft advisories:
	Small Craft Advisory issued May 15 at 2:25PM PDT until May 16 at 6:00AM PDT by NWS Eureka CA
	...
	Small Craft Advisory issued May 15 at 1:49PM PDT until May 16 at 3:00AM PDT by NWS San Francisco CA
	
We could also isolate each individual warning type so that ``isinstance()`` isn't used:

>>> all_alerts = nwsapy.get_alert_by_marine_region('PA')
>>> sca = all_alerts.filter_by('Small Craft Advisory')
>>> hsw = all_alerts.filter_by('Hazardous Seas Warning')
>>> gw = all_alerts.filter_by('Gale Warning')

