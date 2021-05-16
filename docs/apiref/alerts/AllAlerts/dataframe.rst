All Alerts: To Dataframe
========================

.. automethod:: alerts.AllAlerts.to_dataframe
	:noindex:

**Example**

>>> all_alerts = nwsapy.get_all_alerts()
>>> df = all_alerts.to_dataframe()
>>> print(df)
                                                   @id  ...    urgency
0    https://api.weather.gov/alerts/urn:oid:2.49.0....  ...   Expected
1    https://api.weather.gov/alerts/urn:oid:2.49.0....  ...   Expected
..                                                 ...  ...        ...
210  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate
211  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate

