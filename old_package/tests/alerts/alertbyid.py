import unittest
from old_package import errors, nwsapy
from old_package import alerts as al  # this is a bit hackish for test_return_type, but it's needed.


class TestAlertByID(unittest.TestCase):

    def setUp(self):
        nwsapy.set_user_agent("NWSAPy Test", "brandonmolyneaux@tornadotalk.com")
        alerts = nwsapy.get_all_alerts()  # get all of the alerts

        # now we need to get 5 ID's for testing. This is going to prevent us from having to manually get ID's from the
        #   API consistently
        self.list_of_id = [alerts[n].id for n in range(0, 5)]
        self.alert_by_id_one = nwsapy.get_alert_by_id(self.list_of_id[0])
        self.alert_by_id_list = nwsapy.get_alert_by_id(self.list_of_id)  # check with a list of ID's

    def test_return_type(self):
        """Tests to ensure that the return type is correct."""

        # Test with one input
        msg = f"alert_by_id_one not dtype nwsapy.alerts.AlertById. Found: {type(self.alert_by_id_one)}"
        self.assertTrue(isinstance(self.alert_by_id_one, al.AlertById), msg=msg)

        # Test with multiple inputs.
        msg = f"alert_by_id_list not dtype nwsapy.alerts.AlertById. Found: {type(self.alert_by_id_list)}"
        self.assertTrue(isinstance(self.alert_by_id_list, al.AlertById), msg=msg)

    def test_response_header_len_is_same_as_alert(self):
        """Tests to ensure that the response header length is the same as alerts."""

        msg = f"Response header length is not same as alert (single). Alert: {len(self.alert_by_id_one.alerts)}, " \
              f"Response: {len(self.alert_by_id_one.response_headers)}"
        self.assertTrue(len(self.alert_by_id_one.response_headers) == len(self.alert_by_id_one.alerts), msg = msg)

        msg = f"Response header length is not same as alert (list). Alert: {len(self.alert_by_id_list.alerts)}, " \
              f"Response: {len(self.alert_by_id_list.response_headers)}"
        self.assertTrue(len(self.alert_by_id_list.response_headers) == len(self.alert_by_id_list.alerts), msg=msg)
