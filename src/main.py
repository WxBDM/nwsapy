
# Sample script of the UI that the user would have.

import nwsapy

all_alerts = nwsapy.get_alert_count()
atlantic_alerts = all_alerts.filter_land_areas(['ga', 'PA'])
print(atlantic_alerts)


