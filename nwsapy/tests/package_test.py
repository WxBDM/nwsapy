from nwsapy import nwsapy
from pint import UnitRegistry

# Tested and OK: alert_id

a = ['alert_id', 'certainty', 'effective_after', 'effective_before', 'ends_after', 'ends_before', 'event',
     'expires_after', 'expires_before', 'lat_northern_bound', 'lat_southern_bound', 'lon_eastern_bound',
     'lon_western_bound', 'onset_after', 'onset_before', 'sent_after', 'sent_before', 'severity', 'status', 'urgency']

nwsapy.set_user_agent("NWSAPy Test", "brandonmolyneaux@tornadotalk.com")
all_alerts = nwsapy.get_active_alerts()

alerts = all_alerts.filter_by(certainty="Likely")
for alert in alerts:
    print(alert.headline)
