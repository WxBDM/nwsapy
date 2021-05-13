import nwsapy
from shapely.geometry import Point

# Lat/Lon for Arthur, NE.
arthur = Point([-101.6916, 41.5717])  # create a shapely point
all_alerts = nwsapy.get_active_alerts()  # retrieves all active alerts.
svr_tstorms = all_alerts.filter_by('severe thunderstorm warning')

svr_storm1 = svr_tstorms[0]
svr_storm2 = svr_tstorms[1]

if svr_storm1.sent_before(svr_storm2):
    print(f"{svr_storm1.senderName} has sent out a severe warning before {svr_storm2.senderName} has!")
else:
    print(f"{svr_storm2.senderName} has sent out a severe warning before {svr_storm1.senderName} has!")

#
# for alert in all_alerts.alerts: # iterate through the alerts to see if NYC is in any of these alerts.
#     if alert.event == "Test Message": # There's always a test message, ignore it.
#         continue
#
#     if alert.polygon is not None:  # Ensure there is a polygon since we are looking at lat/lon coordinates.
#         is_in = arthur.within(alert.polygon)  # check to see if NYC is in the alert's polygon.
#         issue_time = alert.sent.strftime("%H:%M:%S on %m/%d/%Y")  # extract the sent time from the alert.
#         expire = alert.expires.strftime("%H:%M:%S on %m/%d/%Y") # extract the expiration from the alert.
#         if is_in: # if it's in, print a successful message!
#             print(f'Aurthur, NE is in the {alert.event} sent by {alert.senderName} at {issue_time}, expires at: {expire}')
#         else:  # If not, then print an unsuccessful message.
#             print(f'Aurthur, NE is not in the {alert.event} sent by {alert.senderName} at {issue_time}, expires at: {expire}')
