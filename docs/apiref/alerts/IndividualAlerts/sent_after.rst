Individual Alerts: Sent After
=============================

.. py:method:: sent_after(other)
	:noindex:

	Compares ``self.sent`` to determine if this alert was sent after other.

	:param other: A different alerts.<Alert Event Name> object.
	:type other: alerts.<Alert Event Name>
	:rtype: bool - ``True`` if this alert was sent after other. ``False`` otherwise.
