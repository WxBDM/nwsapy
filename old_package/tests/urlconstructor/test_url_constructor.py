import unittest
from old_package import url_constructor


class TestURLAlert(unittest.TestCase):

    def setUp(self):
        self.alert_urls = url_constructor.AlertURLConstructor()

    def test_one_active_invalid_dtype(self):
        """Tests active parameter raises value error for bad data type."""
        with self.assertRaises(ValueError):
            self.alert_urls.all_alert_url_constructor({'active': "No it isn't!"})
            self.alert_urls.all_alert_url_constructor({'active' : [12345]})
            self.alert_urls.all_alert_url_constructor({'active' : True})
