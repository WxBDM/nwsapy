Alert by Area: Filter By
========================

.. automethod:: alerts.AlertByArea.filter_by
	:noindex:

**Examples**

A simple example stating the number of warnings in Florida, filtered by flood warnings:

>>> all_alerts = nwsapy.get_alert_by_area('FL')
>>> filtered = all_alerts.filter_by("rip current statements")
>>> print(f'There are {len(filtered)} rip current statement(s) active.')
There are 5 rip current statement(s) active.

Let's say we wanted to get the warnings in Florida and surrounding oceans:

>>> all_alerts = nwsapy.get_alert_by_area(['FL', 'GM', 'AM'])
>>> filtered = all_alerts.filter_by("rip current statement")
>>> print(f'There are {len(filtered)} rip current statement(s) active.')
There are 5 rip current statement(s) active.

But if we wanted to filter by multiple alert types:

>>> all_alerts = nwsapy.get_alert_by_area(['FL', 'GM', 'AM'])
>>> all_alerts = all_alerts = nwsapy.get_alert_by_area(['FL', 'GM', 'AM'])
>>> filtered = all_alerts.filter_by(['Small Craft Advisory', 'Rip Current Statement'])
>>> print(f'There are {len(filtered)} small craft advisories and rip current statements.')
There are 15 small craft advisories and rip current statements.

We could also isolate them if we wanted to be more specific:

>>> all_alerts = nwsapy.get_alert_by_area(['FL', 'GM', 'AM'])
>>> all_alerts = all_alerts = nwsapy.get_alert_by_area(['FL', 'GM', 'AM'])
>>> rcs = all_alerts.filter_by('Rip Current Statement')
>>> sca = all_alerts.filter_by(''Small Craft Advisory')
>>> print(f'There are {len(sca)} small craft advisories and {len(rcs)} rip current statements.')
There are 10 small craft advisories and 5 rip current statements.


