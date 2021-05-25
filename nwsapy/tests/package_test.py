from nwsapy import nwsapy

nwsapy.set_user_agent('NWSAPy test', 'test@test.com')
active = nwsapy.get_active_alerts()

storms_one = active.filter_by(event=["Severe Thunderstorm Warning", 'Tornado Warning'], severity='Severe')

storms_two = active.filter_by(event=["Severe Thunderstorm Warning", 'Tornado Warning'])
storms_two = storms_two.filter_by(severity='Severe')

print(f"Number of storms in single filter: {len(storms_one)}\nNumber of storms in double filter: {len(storms_two)}")




