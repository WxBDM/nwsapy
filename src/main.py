
# Sample script of the UI that the user would have.

import nwsapi

active_alerts = nwsapi.get_active_alerts()
all_flood_warnings = active_alerts.filter_by("Flood Warning")





# alert_type = 'Flood Warning'
# # number_of_flood_warnings = active_alerts.get_number_of(321321)  # get the number of flood warnings
# flood_warnings = active_alerts.filter_by(alert_type)  # get the list of just the flood warnings
# flood_warning_first = flood_warnings[0]
#
# print(flood_warning_first.polygon)
