
import noaaobjects as no

def main():

    #  Sample use case for getting the current active alerts.
    alerts = no.get_active_alerts() # this will return an object with all of the active alerts.
    tstorm = alerts.get_all_severe_tstorm_warnings() # returns a list of all of the severe thunderstorm warnings.
    tornado = alerts.get_all_tornado_warnings() # returns a list of all of the tornado warnings



    no.get_alerts()
    no.get_active_alerts()
    no.get_active_alert_by_id(41321312)
    no.get_active_alert_by_state('state')
    no.get_active_alert_by_marine_region("marine_region") # figure out what the regions mean
    no.get_active_alert_by_zone("zoneID")

    #glossary
    no.get_glossary()


if __name__ == "__main__":
    main()


