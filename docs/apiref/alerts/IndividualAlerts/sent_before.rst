Individual Alerts: Sent Before
==============================

.. py:method:: sent_before(other)
	:noindex:

	Compares ``self.sent`` to determine if this alert was sent before other.

	:param other: A different alerts.<Alert Event Name> object.
	:type other: alerts.<Alert Event Name>
	:rtype: bool - ``True`` if this alert was sent before other. ``False`` otherwise.
