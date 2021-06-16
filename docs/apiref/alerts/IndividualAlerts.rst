Individual Alerts
=================

.. currentmodule::nwsapy.alerts

Introduction: Individual Alerts
-------------------------------

Individual alerts are typically found in various alert objects. These objects contain information about a specific alert. For example, if we were to get severe thunderstorm warnings in Pennsylvania and pick out the first warning:

.. code-block:: python

        svr_warnings = nwsapy.get_active_alerts(event = "Severe Thunderstorm Warning", area = "PA")
        first_warning = svr_warnings[0]

This will get us the first severe thunderstorm warning with that criteria:
    >>> print(first_warning.headline)
    Severe Thunderstorm Warning issued June 14 at 6:27PM EDT until June 14 at 7:00PM EDT by NWS Pittsburgh PA

Individual Alert objects themselves are not iterable nor indexable. These objects are generally used for their attributes (see API reference).

The methods that are implemented for :class:`IndividualAlerts` are::

    effective_after(other)
    effective_before(other)
    ends_after(other)
    ends_before(other)
    expires_after(other)
    expires_before(other)
    onset_after(other)
    onset_before(other)
    sent_after(other)
    sent_before(other)
    to_dict()

Where ``other`` is another :class:`IndividualAlert` object.

Individual Alert API Reference
------------------------------

.. autoclass:: nwsapy.alerts.IndividualAlert( )
    :members:
