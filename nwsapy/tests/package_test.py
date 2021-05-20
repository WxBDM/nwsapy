
from nwsapy import nwsapy

nwsapy.set_user_agent("NWSAPy Dev", "test@test.com")

alerts = nwsapy.get_active_alerts()
alerts = alerts.filter_by('Flood Warning')

for alert in alerts:
    print(alert.sent)



