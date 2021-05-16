Individual Alerts: Effective After
==================================

.. py:method:: effective_after(other)
	:noindex:

	Compares ``self.effective`` to determine if this alert is effective after other.

	:param other: A different alerts.<Alert Event Name> object.
	:type other: alerts.<Alert Event Name>
	:rtype: bool - ``True`` if this alert is effective after other. ``False`` otherwise.