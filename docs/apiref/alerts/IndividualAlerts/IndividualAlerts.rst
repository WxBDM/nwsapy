Individual Alerts
=================

When an alerts object is given to you, there's an internal list (can be called by ``.alerts``) containing the individual alerts. Each of these indivual alerts are an object. Thus, ``.alerts`` is a list of individual alert objects. The type is based upon the type of alert it is. For example, an alert for a Frost Advisory would be a ``frostadvisory`` object. Similarily, a tornado warning alert object would be type ``tornadowarning``.

Each alert property is stored as an attribute. So, for example, let's say that we are looking at the following special marine warning in the API web page (note that a lot of information is removed for explaination purposes). We would expect to see something like this:

.. code-block::

	{
	    "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -80.780000000000001,
                            30.129999999999999
                        ],
                        [
                            -81,
                            31.02
                        ],
                        [
                            -80.349999999999994,
                            30.27
                        ],
                        [
                            -80.780000000000001,
                            30.129999999999999
                        ]
                    ]
                ]
            },
	    "properties": {
	        "id": "urn:oid:2.49.0.1.840.0.8dfe228cd0a56af826ab6d7fbc3f40ba82eac48c.002.1",
	        "areaDesc": "Coastal waters from Fernandina Beach to St. Augustine FL out 20 NM; Waters from Altamaha Sound GA to Fernandina Beach FL from 20 to 60 NM; Waters from Fernandina Beach to St. Augustine FL from 20 to 60 NM",
	        "effective": "2021-05-12T17:30:00-04:00",
	        "expires": "2021-05-12T18:45:00-04:00",
	        "status": "Actual",
	        "messageType": "Update",
	        "severity": "Severe",
	        "event": "Special Marine Warning",
	        "senderName": "NWS Jacksonville FL",
	        "headline": "Special Marine Warning issued May 12 at 5:30PM EDT until May 12 at 6:45PM EDT by NWS Jacksonville FL",
	        "description": "For the following areas...\nCoastal waters from Fernandina Beach to St. Augustine FL out 20 NM...\nWaters from Altamaha Sound GA to Fernandina Beach FL from 20 to 60\nNM...\nWaters from Fernandina Beach to St. Augustine FL from 20 to 60 NM...\n\nAt 529 PM EDT, showers and thunderstorms were located along a\nline extending from 20 nm southeast of R2 Tower to 23 nm east of\nGuana River State Park, moving southeast at 30 knots.\n\nHAZARD...Wind gusts 34 knots or greater.\n\nSOURCE...Radar indicated.\n\nIMPACT...Small craft could be damaged in briefly higher winds and\nsuddenly higher waves.\n\nLocations impacted include...\nBuoy Hlha, Tournament Reef, Casablanca Reef and Anna Reef.",
	    }
	}

When created, this specific alert would have the following attributes from ``geometry``:

	| ``.polygon``
	| ``.points``
	| ``.point_collection``

This specific alert would have the following attributes from ``properties``:

	| ``.id`` 
	| ``.areaDesc``
	| ``.effective``
	| ``.expires``
	| ``.status``
	| ``.messageType``
	| ``.severity``
	| ``.event``
	| ``.senderName``
	| ``.headline``
	| ``.description``

.. attention:: Unless otherwise stated below, all attributes for individual alerts are strings.

	| ``.polygon`` (shapely.Polygon)
	| ``.points`` (list of shapely.Point)
	| ``.point_collection`` (shapely.Multipoint)
	| ``.sent`` (datetime.datetime)
	| ``.effective`` (datetime.datetime)
	| ``.onset`` (datetime.datetime)
	| ``.expires`` (datetime.datetime)
	| ``.ends`` (datetime.datetime)
	
	Note that some of the above attributes could also be ``None``.

.. _individual_alerts_error:

Individual Alerts: Error
------------------------

Sometimes, you'll receive an error. Most of the time, it will be a 404 error (and for those not familiar with these kinds of errors, 404 is ``not found``). NWSAPy can't prevent you from getting 404 errors, but there are built-in checks to ensure that 404 errors are minimized.

If you were to receive an error, the JSON format would look as such:

.. code-block::

	{
	    "correlationId": "3dff7cd2",
	    "title": "Zone Does Not Exist",
	    "type": "https://api.weather.gov/problems/InvalidZone",
	    "status": 404,
	    "detail": "Forecast zone NVZ does not exist",
	    "instance": "https://api.weather.gov/requests/3dff7cd2"
	}
	
Which, in turn, would translate to the following attributes:

	| ``.correlationId``
	| ``.title``
	| ``.type``
	| ``.status``
	| ``.detail``
	| ``.instance``
	| ``.event``

Individual Alert API Reference
------------------------------

Error
^^^^^

.. py:class:: alerts.error

	An error object explaining the error. This error is typically a 404, but also could be 500.
	
	.. attribute:: correlationId
		:type: str
	
	.. attribute:: title
		:type: str
	
	.. attribute:: type
		:type: str
	
	.. attribute:: status
		:type: int
	
	.. attribute:: detail
		:type: str
	
	.. attribute:: instance
		:type: str
	
	.. attribute:: event
		:type: str or None

Individual Alert
^^^^^^^^^^^^^^^^

.. _dynamically-created-alerts:
.. py:class:: alerts.<Alert Event Name>

   A dynamically created alert, with ``<Alert Event Name>`` being the name of the alert.
   
   For example, if the event is a tornado warning, the name of the dynamically created alert would be ``alerts.tornadowarning``. Similarily, for a small craft advisory, it would be ``alerts.smallcraftadvisory``, and so forth.
   
   	.. attribute:: affectedZones
		:type: str
	
	.. attribute:: areaDesc
		:type: str
	
	.. attribute:: category
		:type: str
	
	.. attribute:: description
		:type: str
	
	.. attribute:: effective
		:type: datetime.datetime
	
	.. attribute:: ends
		:type: datetime.datetime
	
	.. attribute:: event
		:type: str
	
	.. attribute:: effective
		:type: datetime.datetime
		:noindex:
	
	.. attribute:: geocode
		:type: dict
	
	.. attribute:: headline
		:type: str
	
	.. attribute:: id
		:type: str
	
	.. attribute:: instruction
		:type: str
	
	.. attribute:: messageType
		:type: str
	
	.. attribute:: onset
		:type: datetime.datetime
	
	.. attribute:: parameters
		:type: dict
	
	.. attribute:: points
		:type: list, containing shapely.Point
	
	.. attribute:: points_collection
		:type: shapely.MultiPoint
	
	.. attribute:: polygon
		:type: shapely.Polygon
	
	.. attribute:: references
		:type: dict
	
	.. attribute:: sender
		:type: str
	
	.. attribute:: senderName
		:type: str
	
	.. attribute:: sent
		:type: datetime.datetime
	
	.. attribute:: series
		:type: str
	
	.. attribute:: severity
		:type: str
	
	.. attribute:: status
		:type: str
	
	.. attribute:: urgency
		:type: str
	
	.. py:method:: sent_before(other)
	
		Compares ``self.sent`` to determine if this alert was sent before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was sent before other. ``False`` otherwise.
   
	.. py:method:: sent_after(other)

		Compares ``self.sent`` to determine if this alert was sent after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was sent after other. ``False`` otherwise.
	
	.. py:method:: effective_before(other)
	
		Compares ``self.effective`` to determine if this alert is effective before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert is effective before other. ``False`` otherwise.
   
	.. py:method:: effective_after(other)

		Compares ``self.effective`` to determine if this alert is effective after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert is effective after other. ``False`` otherwise.

	.. py:method:: onset_before(other)
	
		Compares ``self.onset`` to determine if this alert was onset before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was onset before other. ``False`` otherwise.
   
	.. py:method:: onset_after(other)

		Compares ``self.onset`` to determine if this alert was onset after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert was onset after other. ``False`` otherwise.
	
	.. py:method:: expires_before(other)
	
		Compares ``self.expires`` to determine if this alert will expire before other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert will expire before other. ``False`` otherwise.
   
	.. py:method:: expires_after(other)

		Compares ``self.expires`` to determine if this alert will expire after other.
	
		:param other: A different alerts.<Alert Event Name> object.
		:type other: alerts.<Alert Event Name>
		:rtype: bool - ``True`` if this alert will expire after other. ``False`` otherwise.
   

.. toctree::
	:hidden:
	
	alerts.<Event Name>.sent_before <sent_before>
	alerts.<Event Name>.sent_after <sent_after>
	alerts.<Event Name>.effective_before <effective_before>
	alerts.<Event Name>.effective_after <effective_after>
	alerts.<Event Name>.onset_before <onset_before>
	alerts.<Event Name>.onset_after <onset_after>
	alerts.<Event Name>.expires_before <expires_before>
	alerts.<Event Name>.expires_after <expires_after>
