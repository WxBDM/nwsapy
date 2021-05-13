
# Sample script of the UI that the user would have.

import nwsapy

active_alerts = nwsapy.get_active_alerts()
flood_warnings = active_alerts.filter_by("Flood Warning")
first_flood_warning = flood_warnings[0]
print(first_flood_warning.peek_at_info())
