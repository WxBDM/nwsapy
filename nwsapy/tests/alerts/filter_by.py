import unittest
from nwsapy import errors, nwsapy


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
        '''Tests without any kwargs for filter. Expected: ParameterTypeError'''
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by()

    def test_expected_list_is_empty(self):
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by(event= [])
            self.alerts.filter_by(urgency= [])
            self.alerts.filter_by(severity= [])
            self.alerts.filter_by(certainty= [])

    def test_times_not_datetime_obj(self):
        """Tests to ensure that an errors.ParameterTypeError has been raised for parameters that have to be datetime
            objects.
        """
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by(effective_before= 'effective_before')
            self.alerts.filter_by(effective_after= 'effective_after')
            self.alerts.filter_by(ends_before='ends_before')
            self.alerts.filter_by(ends_after='ends_after')
            self.alerts.filter_by(expires_before='expires_before')
            self.alerts.filter_by(expires_after='expires_after')
            self.alerts.filter_by(onset_before='onset_before')
            self.alerts.filter_by(onset_after='onset_after')
            self.alerts.filter_by(sent_before='sent_before')
            self.alerts.filter_by(sent_after='sent_after')

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
            self.alerts.filter_by(event="Not a valid NWS event!")
            self.alerts.filter_by(urgency="Not a valid urgency input! it must not be that urgent!")
            self.alerts.filter_by(severity="Not a valid severity level!")
            self.alerts.filter_by(certainty="Not a valid certainty level!")

    def test_data_validation_is_right_but_formatted_wrong(self):
        """Tests to ensure that the data is formatted properly."""

        self.alerts.filter_by(event="sEvEre tHunderStorm wArnIng")
        self.alerts.filter_by(severity="mInor")
        self.alerts.filter_by(urgency="pAst")
        self.alerts.filter_by(certainty="lIkeLy")

    def test_alert_id_param(self):
        """Tests to ensure that the alerts are getting filtered by id."""
        # test an individual one. Since this is dynamic, just get the first n.
        should_be_one_alert = self.alerts.filter_by(alert_id=self.alerts[0].id)
        self.assertEquals(len(should_be_one_alert), 1, f"alert_id is not length 1. Got: {len(should_be_one_alert)}")

        # test multiple alerts.
        should_be_three_alerts = self.alerts.filter_by(alert_id = [self.alerts[x].id for x in range(0, 3)])
        self.assertEquals(len(should_be_three_alerts), 3, f"alert_id is not length 3. Got: {len(should_be_three_alerts)}")

        # test if it's invalid alert, should return a length of 0.
        should_be_none = self.alerts.filter_by(alert_id = "None! :)")
        self.assertEquals(len(should_be_none), 0, f"alert_id is not length 0. Got: {len(should_be_none)}")

        # test to make sure the alert is a string, raises ParameterTypeError.
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by(alert_id = 321312)
            self.alerts.filter_by(alert_id = 12.132)
            self.alerts.filter_by(alert_id = (32, "TDD is a pain sometimes."))
            self.alerts.filter_by(alert_id = ['a list?', 'heck yes.'])

    def test_certainty_param(self):
        pass


if __name__ == '__main__':
    unittest.main()