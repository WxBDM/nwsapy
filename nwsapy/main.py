import nwsapy


def main():
    nwsapy.set_user_agent("NWSAPy User", "test@test.com")

    zone_alert = nwsapy.get_alert_by_zone("NVZ031")
    print(zone_alert)
    all_alerts = nwsapy.get_all_alerts()
    print(all_alerts)
    active_alerts = nwsapy.get_active_alerts()
    print(active_alerts)
    types = nwsapy.get_alert_types()
    print(types)
    alert_id = nwsapy.get_alert_by_id("urn:oid:2.49.0.1.840.0.e…7c84fbc7ed18af42b.001.1")
    print(alert_id)
    counts = nwsapy.get_alert_count()
    print(counts)
    area = nwsapy.get_alert_by_area('AL')
    print(area)
    marine = nwsapy.get_alert_by_marine_region('AL')
    print(marine)


if __name__ == "__main__":
    main()