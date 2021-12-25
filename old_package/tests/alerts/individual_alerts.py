import unittest
from datetime import datetime

from old_package import nwsapy
import pandas as pd
import random
import shapely


class IndividualAlerts(unittest.TestCase):

    def setUp(self):
        nwsapy.set_user_agent("NWSAPy Test - Individual Alerts", "brandonmolyneaux@tornadotalk.com")
        self.alerts = nwsapy.get_all_alerts()
        r = random.randint(0, len(self.alerts))
        self.sample_alert = self.alerts[r]

    def test_all_attributes(self):
        """Tests to make sure all attributes in each alert exists."""
        attributes = ['affectedZones', 'areaDesc', 'category', 'certainty', 'description', 'effective', 'effective_utc',
                      'ends', 'ends_utc', 'event', 'expires', 'expires_utc', 'geocode', 'headline', 'id', 'instruction',
                      'messageType', 'onset', 'onset_utc', 'parameters', 'points', 'polygon', 'references', 'response',
                      'sender', 'senderName', 'sent', 'sent_utc', 'series', 'severity', 'status', 'urgency']

        for n_alert, alert in enumerate(self.alerts):
            for attr in attributes:
                hasAttr = hasattr(alert, attr)
                self.assertTrue(hasAttr, msg=f"{alert.event} does not have attribute {attr} (alert #: {n_alert})")

    def test_datatype_attribute_datetime(self):
        """Tests data type for all times."""

        for alert in self.alerts:  # iterate through each one :)
            alert_test_d = {'effective': [alert.effective, alert.effective_utc],
                            'ends': [alert.ends, alert.ends_utc],
                            'onset': [alert.onset, alert.onset_utc],
                            'sent': [alert.sent, alert.sent_utc],
                            'exprires': [alert.expires, alert.expires_utc]
                            }

            for which_alert in alert_test_d:
                attributes = alert_test_d[which_alert]
                value_non_utc = attributes[0]
                value_utc = attributes[1]

                # test non-utc attribute
                msg = f"{which_alert} LOCAL dtype (expected datetime.datetime or None): {type(value_non_utc)}\nVal: " \
                      f"{value_non_utc}"
                valid = [isinstance(value_non_utc, datetime), isinstance(value_non_utc, type(None))]
                self.assertTrue(any(valid),
                                msg=msg)

                # test utc attribute
                if value_utc is not None:
                    msg = f"{which_alert}_utc time not UTC. Got: {value_utc.tzinfo}\nVal: {value_utc}"
                    self.assertTrue(str(attributes[1].tzinfo) == "UTC", msg=msg)
                else:
                    msg = f"{which_alert}_utc is not None (found: non-utc version is none).\nVal: {value_utc}\n" \
                          f"Dtype: {type(value_utc)}"
                    self.assertTrue(isinstance(value_utc, type(None)), msg=msg)

    def test_datatype_attribute_string(self):
        """Tests for string data type."""

        for n, alert in enumerate(self.alerts):
            test_d = {'category' : alert.category, 'certainty' : alert.certainty, 'description' : alert.description,
                      'event' : alert.event, 'headline' : alert.headline, 'id' : alert.id,
                      'instruction' : alert.instruction, 'messageType' : alert.messageType, 'response' : alert.response,
                      'sender' : alert.sender, 'senderName' : alert.senderName, 'severity' : alert.severity,
                      'status' : alert.status, 'urgency' : alert.urgency
                     }

            for element in test_d:
                attribute = test_d[element]
                msg = f"{element} dtype (expected str): {type(attribute)}\nVal: {attribute}\nnth: {n} " \
                      f"event: {alert.event}"
                self.assertTrue(isinstance(attribute, str), msg=msg)

    def test_attribute_dtype_list_of_str(self):

        for alert in self.alerts:
            alert = self.alerts[0]  # just get the first one, reduces time complexity + alerts obj is the same for all.
            if alert.event == 'Test Message':  # skip the test message. Future update: remove the test message?
                alert = self.alerts[1]

            test_d = {'Affected zones' : alert.affectedZones, 'Area description' : alert.areaDesc}

            for attribute in test_d:
                value = test_d[attribute]
                msg = f"{attribute} dtype (expected list): {type(value)}\nValue: {value}"
                self.assertTrue(isinstance(value, list), msg=msg)
                for n, zone in enumerate(value):  # iterate through all and ensure they're a string.
                    msg = f"Affected zones dtype (expected str): {type(zone)} (index {n})\n Value: {zone}"
                    self.assertTrue(isinstance(zone, str), msg=msg)

    def test_attribute_dtype_other(self):
        """Tests other alerts."""

        for alert in self.alerts:
            test_d = {'geocode': [alert.geocode, dict],
                      'parameters': [alert.parameters, dict],
                      'references': [alert.references, list],
                      'points': [alert.points, list],
                      'polygon': [alert.polygon, shapely.geometry.polygon.Polygon],
                      'series': [alert.series, pd.Series]
                      }

            for attribute in test_d:
                value_info = test_d[attribute]
                value = value_info[0]
                dtype = value_info[1]

                msg = f"{attribute} is not of type {dtype}. Got: {type(value)}. Value: {value}"
                valid = (isinstance(value, dtype), isinstance(value, type(None)))
                self.assertTrue(any(valid), msg = msg)
