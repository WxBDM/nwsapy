Individual Alerts: Expires Before
=================================

.. py:method:: expires_before(other)
	:noindex:

	Compares ``self.expires`` to determine if this alert will expire before other.

	:param other: A different alerts.<Alert Event Name> object.
	:type other: alerts.<Alert Event Name>
	:rtype: bool - ``True`` if this alert will expire before other. ``False`` otherwise.
