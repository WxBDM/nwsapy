Alert by Area: To Dataframe
===========================

.. automethod:: alerts.AlertByArea.to_dataframe
	:noindex:

**Example**

>>> all_alerts = nwsapy.get_alert_by_area('CO')
>>> df = all_alerts.to_dataframe()
>>> print(df)
                                                 @id  ...    urgency
0  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...   Expected
1  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate
2  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Immediate
3  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...     Future
4  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...     Future
5  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...     Future
6  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...     Future

