import unittest
from nwsapy import *  # just import everything why not


class TestSum(unittest.TestCase):

    def setUp(self):
        nwsapy.set_user_agent("NWSAPy Test", "brandonmolyneaux@tornadotalk.com")
        self.alerts = nwsapy.get_all_alerts()  # get all of the alerts
        self.active_alerts = nwsapy.get_active_alerts() # get active alerts
        self.area = nwsapy.get_alert_by_area('TX') # get a list of

    # testing data types!
    def test_if_alerts_raise_(self):
        """Tests to ensure that alerts are iterable."""
        for alert in self.alerts:
            print(type(alert))


if __name__ == '__main__':
    unittest.main()

