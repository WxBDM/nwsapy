Active Alerts: To Dataframe
===========================

.. currentmodule:: nwsapy.alerts
.. automethod:: ActiveAlerts.to_dataframe
	:noindex:

**Example**

>>> all_alerts = nwsapy.get_active_alerts()
>>> df = all_alerts.to_dataframe()
>>> print(df)
                                                   @id  ...    urgency
0    https://api.weather.gov/alerts/urn:oid:2.49.0....  ...    Unknown
1    https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate
..                                                 ...  ...        ...
216  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate
217  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate


