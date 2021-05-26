import unittest
from datetime import datetime
from nwsapy import errors, nwsapy
from nwsapy import alerts as al


class TestFilterBy(unittest.TestCase):

    def setUp(self):
        nwsapy.set_user_agent("NWSAPy Test", "brandonmolyneaux@tornadotalk.com")
        self.alerts = nwsapy.get_all_alerts()  # get all of the alerts

    def test_list_only_contains_flood_warnings(self):
        alerts = self.alerts.filter_by(event = "Flood warning")
        test_alert = type(alerts[0]) # had to go about doing this slightly different.
        for alert in alerts[1:]:
            self.assertTrue(isinstance(alert, test_alert)) # if a = b, and b = c, then a = c

    # testing data types!
    def test_no_kwargs_filter(self):
        '''Tests without any kwargs for filter. Expected: Parameter'''
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by()

    def test_values_not_boolean(self):
        """Tests to ensure that an errors.ParameterTypeError has been raised for parameters that have to be boolean

        Parameters: active
        """
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by(active = 'this is active')

    def test_times_not_datetime_obj(self):
        """Tests to ensure that an errors.ParameterTypeError has been raised for parameters that have to be datetime
            objects.

        Parameters: start_time, end_time
        """
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by(start_time = 'start time')
            self.alerts.filter_by(end_time = 'end time')

    def test_ParameterTypeError(self):
        """Tests to ensure that an errors.ParameterTypeError has been raised for all parameters

        Parameters: status, message_type, event, region_type, point, region, area, zone, urgency, severity, certainty

        Tests against built in data structures
        """

        test_values = (1231321, {"This is a " : f"Dictionary"}, True, 111.22, type('DCO', (), {}))

        for test_type in test_values: # Tuples, lists, and strings are all valid for these.
            with self.assertRaises(errors.ParameterTypeError):
                self.alerts.filter_by(alert_id = test_type)
                self.alerts.filter_by(certainty = test_type)
                self.alerts.filter_by(effective_after = test_type)
                self.alerts.filter_by(effective_before  = test_type)
                self.alerts.filter_by(ends_after = test_type)
                self.alerts.filter_by(ends_before = test_type)
                self.alerts.filter_by(event = test_type)
                self.alerts.filter_by(expires_after  = test_type)
                self.alerts.filter_by(expires_before = test_type)
                self.alerts.filter_by(onset_after = test_type)
                self.alerts.filter_by(onset_before = test_type)
                self.alerts.filter_by(sent_after = test_type)
                self.alerts.filter_by(sent_before = test_type)
                self.alerts.filter_by(severity = test_type)
                self.alerts.filter_by(status = test_type)
                self.alerts.filter_by(urgency = test_type)

        test_values = ("This is a string", ['A list of strings!'], ('tuple!',),
                       {"This is a ": f"Dictionary"}, True, type('DCO', (), {}))

        for test_type in test_values: # Integers of 4 digits should only be allowed.
            with self.assertRaises(errors.ParameterTypeError):
                self.alerts.filter_by(lat_northern_bound = test_type)
                self.alerts.filter_by(lat_southern_bound = test_type)
                self.alerts.filter_by(lon_eastern_bound = test_type)
                self.alerts.filter_by(lon_western_bound = test_type)

    def test_data_validation_error(self):
        """Tests to make sure a data validation error appears.

        Parameters: event, message_type, status, event, region_type, area, zone, urgency, severity, certainty
        """
        with self.assertRaises(errors.DataValidationError):
            self.alerts.filter_by(status = "Not a valid status!")
            self.alerts.filter_by(message_type="Not a valid message type!")
            self.alerts.filter_by(status="Not a valid status!")
            self.alerts.filter_by(event="Not a valid NWS event!")
            self.alerts.filter_by(region_type="Not a valid region type!")
            self.alerts.filter_by(area="Not a valid NWS area!")
            self.alerts.filter_by(zone="Not a valid NWS event!") # TODO: data validation table for this.
            self.alerts.filter_by(urgency="Not a valid urgency input! it must not be that urgent!")
            self.alerts.filter_by(severity="Not a valid severity level!")
            self.alerts.filter_by(certainty="Not a valid certainty level!")

    def test_data_validation_is_right_but_formatted_wrong(self):
        """Tests to ensure that the data is formatted properly."""

        self.alerts.filter_by(status = "SyStEm")
        self.alerts.filter_by(message_type="aLeRt")
        self.alerts.filter_by(event="sEvEre tHunderStorm wArnIng")
        self.alerts.filter_by(severity="mInor")
        self.alerts.filter_by(urgency="pAst")
        self.alerts.filter_by(certainty="lIkeLy")

    def test_return_type(self):
        """Tests to make sure return type is correct. Note: This only tests get_all_alerts()"""

        new_alerts = self.alerts.filter_by(active = True)  # successful filter option, filter it.
        unsuccessful_msg = f"Return type is not correct. Expected: {type(self.alerts)}, got: {type(new_alerts)}"
        self.assertEqual(type(new_alerts), type(self.alerts), unsuccessful_msg)


if __name__ == '__main__':
    unittest.main()