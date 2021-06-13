from nwsapy import url_constructor
from nwsapy import nwsapy

nwsapy.set_user_agent("NWSAPy Test", "brandonmolyneaux@tornadotalk.com")
alerts = nwsapy.get_all_alerts(active=True, event=['Severe Thunderstorm Warning'])
all_alerts = nwsapy.get_all_alerts()

print(len(alerts))
print(len(all_alerts))