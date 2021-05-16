Alert by Marine Region: To Dataframe
====================================

.. automethod:: alerts.AlertByMarineRegion.to_dataframe
	:noindex:

**Example**

>>> all_alerts = nwsapy.get_alert_by_marine_region('AL')
>>> df = all_alerts.to_dataframe()
>>> print(df)
                                                  @id  ...   urgency
0   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
1   https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
...
21  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
22  https://api.weather.gov/alerts/urn:oid:2.49.0....  ...  Expected
