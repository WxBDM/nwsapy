import unittest
from datetime import datetime
from nwsapy import errors, nwsapy
from nwsapy import alerts as al
import pandas as pd


class TestSum(unittest.TestCase):

    def setUp(self):
        nwsapy.set_user_agent("NWSAPy Test - Individual Alerts", "brandonmolyneaux@tornadotalk.com")
        self.alerts = nwsapy.get_all_alerts()

    def test_all_attributes(self):
        """Tests to make sure all attributes in each alert exists."""
        attributes = ['affectedZones', 'areaDesc', 'category', 'certainty', 'description', 'effective', 'effective_utc',
                      'ends', 'ends_utc', 'event', 'expires', 'expires_utc', 'geocode', 'headline', 'id', 'instruction',
                      'messageType', 'onset', 'onset_utc', 'parameters', 'points', 'polygon', 'references', 'response',
                      'sender', 'senderName', 'sent', 'sent_utc', 'series', 'severity', 'status', 'urgency']

        for n_alert, alert in enumerate(self.alerts):
            for attr in attributes:
                hasAttr = hasattr(alert, attr)
                self.assertTrue(hasAttr, msg = f"{alert.event} does not have attribute {attr} (alert #: {n_alert})")

    def test_datatype_for_attributes(self):
        """Data types for individual alerts are checked"""

        alert = self.alerts[0] # just get the first one, reduces time complexity + alerts obj is the same for all.
        if alert.event == 'Test Message': # skip the test message. Future update: remove the test message?
            alert = self.alerts[1]

        # zones - list[str]: ['AZK001']
        self.assertTrue(isinstance(alert.affectedZones, list),
                        msg = f"Affected zones dtype (expected list): {type(alert.affectedZones)}\n"
                              f"Value: {alert.affectedZones}")
        for n, zone in enumerate(alert.affectedZones):
            self.assertTrue(isinstance(zone, str),
                            msg = f"Affected zones dtype (expected str): {type(zone)} (index {n})\n Value: {zone}")

        # areaDesc - list[str]: ['The waters off of the state', 'Pampa, TX']
        self.assertTrue(isinstance(alert.areaDesc, list),
                        msg = f"Area Description dtype (expected list): {type(alert.affectedZones)}")
        for n, desc in enumerate(alert.areaDesc):
            self.assertTrue(isinstance(desc, str),
                            msg = f"Area Description dtype (expected str) {type(desc)} (index {n})") # each element is a string.

        # category - str: 'Met'
        self.assertTrue(isinstance(alert.category, str),
                        msg=f"Category dtype (expected str): {type(alert.category)}\nVal: {alert.category}")

        # certainty - str: 'Likely'
        self.assertTrue(isinstance(alert.certainty, str),
                        msg=f"Certainty dtype (expected str): {type(alert.certainty)}\nVal: {alert.certainty}")

        # description - str: 'Flood warning!'
        self.assertTrue(isinstance(alert.description, str),
                        msg=f"Description dtype (expected str): {type(alert.description)}\nVal: {alert.description}")

        # effective - datetime: datetime.datetime(2020, 4, 20, 13, 20) LOCAL TIME
        self.assertTrue(isinstance(alert.effective, str),
                        msg=f"Effective LOCAL dtype (expected datetime): {type(alert.effective)}\nVal: {alert.effective}")
        self.assertTrue(str(alert.effective.tztime) != "UTC",
                        msg=f"Effective LOCAL time not UTC. Got: {alert.effective.tztime}")

        # effective_utc - datetime: datetime.datetime(2020, 4, 20, 13, 20) UTC TIME
        self.assertTrue(isinstance(alert.effective_utc, str))
        self.assertTrue(str(alert.effective_utc.tztime) == "UTC")

        # ends - datetime: datetime.datetime(2020, 4, 20, 13, 20) LOCAL TIME
        self.assertTrue(isinstance(alert.ends, str))
        self.assertTrue(str(alert.ends.tztime) != "UTC")

        # ends_utc - datetime: datetime.datetime(2020, 4, 20, 13, 20) UTC TIME
        self.assertTrue(isinstance(alert.ends_utc, str))
        self.assertTrue(str(alert.ends_utc.tztime) == "UTC")

        # event - str: 'Flood Warning'
        self.assertTrue(isinstance(alert.event, str))

        # expires - datetime: datetime.datetime(2020, 4, 20, 13, 20) LOCAL TIME
        self.assertTrue(isinstance(alert.expires, str))
        self.assertTrue(str(alert.expires.tztime) != "UTC")

        # expires_utc - datetime: datetime.datetime(2020, 4, 20, 13, 20) UTC TIME
        self.assertTrue(isinstance(alert.expires_utc, str))
        self.assertTrue(str(alert.expires_utc.tztime) == "UTC")

        # geocode - dict: {} not worried too much about this one
        self.assertTrue(isinstance(alert.geocode, dict))

        # headline - str: 'Flood Warning has been issued'
        self.assertTrue(isinstance(alert.headline, str))

        # id - str: "urn:oid:2.49.0.1.840.0.b…3503c8a878c6d2326.001.1"
        self.assertTrue(isinstance(alert.id, str))

        # instruction - str: "Turn around and don't drown"
        self.assertTrue(isinstance(alert.instruction, str))

        # messageType - str: "Update"
        self.assertTrue(isinstance(alert.messageType, str))

        # onset - datetime: datetime.datetime(2020, 4, 20, 13, 20) LOCAL TIME
        self.assertTrue(isinstance(alert.onset, str))
        self.assertTrue(str(alert.onset.tztime) != "UTC")

        # onset_utc - datetime: datetime.datetime(2020, 4, 20, 13, 20) UTC TIME
        self.assertTrue(isinstance(alert.onset_utc, str))
        self.assertTrue(str(alert.onset_utc.tztime) == "UTC")

        # parameters - dict: {} not worried about this one
        self.assertTrue(isinstance(alert.parameters, dict))

        # points - shapely.geometry.Point: Point([-88, 30]) shapely is backwards >:(
        # polygon - shapely.geometry.Polygon: collection of points
        # references - list: [] not worried about this one.
        self.assertTrue(isinstance(alert.references, list))

        # response - str: "Avoid"
        self.assertTrue(isinstance(alert.response, str))

        # sender - str: "w-nws.webmaster@noaa.gov" I haven't seen a sender aside from this.
        self.assertTrue(isinstance(alert.sender, str))

        # senderName - str: "NWS Shreveport LA"
        self.assertTrue(isinstance(alert.senderName, str))

        # sent - datetime: datetime.datetime(2020, 4, 20, 13, 20) LOCAL TIME
        self.assertTrue(isinstance(alert.sent, str))
        self.assertTrue(str(alert.sent.tztime) != "UTC")

        # sent_utc - datetime: datetime.datetime(2020, 4, 20, 13, 20) UTC TIME
        self.assertTrue(isinstance(alert.sent_utc, str))
        self.assertTrue(str(alert.sent_utc.tztime) == "UTC")

        # series - pd.Series
        self.assertTrue(isinstance(alert.series, type(pd.Series())))

        # severity - str: "Severe"
        self.assertTrue(isinstance(alert.severity, str))

        # status - str: "Actual"
        self.assertTrue(isinstance(alert.status, str))

        # urgency - str: "Immediate"
        self.assertTrue(isinstance(alert.urgency, str))


if __name__ == '__main__':
    unittest.main()
