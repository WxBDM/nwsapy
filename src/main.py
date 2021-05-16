import nwsapy
import utils
from shapely.geometry import Point


def main():
    nwsapy.set_user_agent("NWSAPy User", "test@test.com")

    active_alerts = nwsapy.get_active_alerts()
    alert = active_alerts.alerts[1]

if __name__ == "__main__":
    main()