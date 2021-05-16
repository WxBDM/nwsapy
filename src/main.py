import nwsapy
import utils
from shapely.geometry import Point


def main():
    nwsapy.set_user_agent("NWSAPy User", "test@test.com")

    active_alerts = nwsapy.get_alert_by_zone("NVZ031")
    print(active_alerts[0])

if __name__ == "__main__":
    main()