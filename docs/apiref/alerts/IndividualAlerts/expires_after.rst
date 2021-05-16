Individual Alerts: Expires After
================================

.. py:method:: expires_after(other)
	:noindex:

	Compares ``self.expires`` to determine if this alert will expire after other.

	:param other: A different alerts.<Alert Event Name> object.
	:type other: alerts.<Alert Event Name>
	:rtype: bool - ``True`` if this alert will expire after other. ``False`` otherwise.
