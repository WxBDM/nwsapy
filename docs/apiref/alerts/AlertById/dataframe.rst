Alerts by ID: To Dataframe
==========================

.. automethod:: alerts.AlertById.to_dataframe
	:noindex:

**Example**

>>> all_alerts = nwsapy.get_alert_by_id('urn:oid:2.49.0.1.840.0.050e935e72efe1d507886e3b5e8ddc619f494f6a.001.1')
>>> df = all_alerts.to_dataframe()
>>> print(df)
                                                 @id  ...    urgency
0  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate

