import unittest
from datetime import datetime
from nwsapy import errors, nwsapy


class TestSum(unittest.TestCase):

    def setUp(self):
        nwsapy.set_user_agent("NWSAPy Test", "brandonmolyneaux@tornadotalk.com")
        self.alerts = nwsapy.get_all_alerts()  # get all of the alerts

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

    def test_values_not_string(self):
        """Tests to ensure that an errors.ParameterTypeError has been raised for parameters that are strings.

        Parameters: status, message_type, event, region_type, point, region, area, zone, urgency, severity, certainty

        Tests against built in data structures
        """
        with self.assertRaises(errors.ParameterTypeError):
            self.alerts.filter_by(status = ["this is status"])
            self.alerts.filter_by(status=("this is status",))
            self.alerts.filter_by(status=123345)
            self.alerts.filter_by(status={"this is ": "status"})
            self.alerts.filter_by(status=True)
            self.alerts.filter_by(message_type = ["this is message type"])
            self.alerts.filter_by(message_type=("this is message type",))
            self.alerts.filter_by(message_type=123345)
            self.alerts.filter_by(message_type=321.999)
            self.alerts.filter_by(message_type={"this is ": "message_type"})
            self.alerts.filter_by(message_type=True)
            self.alerts.filter_by(event = ["This is events"])
            self.alerts.filter_by(event=("this is events",))
            self.alerts.filter_by(event=123345)
            self.alerts.filter_by(event=321.999)
            self.alerts.filter_by(event={"this is ": "event"})
            self.alerts.filter_by(event=True)
            self.alerts.filter_by(region_type=["this is region_type"])
            self.alerts.filter_by(region_type=("this is region type",))
            self.alerts.filter_by(region_type=123345)
            self.alerts.filter_by(region_type=321.999)
            self.alerts.filter_by(region_type={"this is ": "region type"})
            self.alerts.filter_by(region_type=True)
            self.alerts.filter_by(point=["this is point"])
            self.alerts.filter_by(point=("this is point",))
            self.alerts.filter_by(point=123345)
            self.alerts.filter_by(point=321.999)
            self.alerts.filter_by(point={"this is ": "point"})
            self.alerts.filter_by(point=True)
            self.alerts.filter_by(region=["This is region"])
            self.alerts.filter_by(region=("this is region",))
            self.alerts.filter_by(region=123345)
            self.alerts.filter_by(region=321.999)
            self.alerts.filter_by(region={"this is ": "region"})
            self.alerts.filter_by(region=True)
            self.alerts.filter_by(area=["this is zone"])
            self.alerts.filter_by(area=("this is area",))
            self.alerts.filter_by(area=123345)
            self.alerts.filter_by(area=321.999)
            self.alerts.filter_by(area={"this is ": "area"})
            self.alerts.filter_by(area=True)
            self.alerts.filter_by(urgency=["this is urgency"])
            self.alerts.filter_by(urgency=("this is urgency",))
            self.alerts.filter_by(urgency=123345)
            self.alerts.filter_by(urgency=321.999)
            self.alerts.filter_by(urgency={"this is ": "urgency"})
            self.alerts.filter_by(urgency=True)
            self.alerts.filter_by(severity=["This is severity"])
            self.alerts.filter_by(severity=("this is severity",))
            self.alerts.filter_by(severity=123345)
            self.alerts.filter_by(severity=321.999)
            self.alerts.filter_by(severity={"this is ": "severity"})
            self.alerts.filter_by(severity=True)
            self.alerts.filter_by(certainty=["This is certainty"])
            self.alerts.filter_by(certainty=("this is certainty",))
            self.alerts.filter_by(certainty=123345)
            self.alerts.filter_by(certainty=321.999)
            self.alerts.filter_by(certainty={"this is ": "certainty"})
            self.alerts.filter_by(certainty=True)

    def test_conflicting_values(self):
        """Tests to ensure that an errors.ParameterConflict error appears if 2 or more parameters conflict with
        eachother.

        Conflicting parameters: region_type, point, region, area, zone"""

        with self.assertRaises(errors.ParameterConflict):
            # Region type with all
            self.alerts.filter_by(region_type='land', point = '39,-99')
            self.alerts.filter_by(region_type='marine', region='AL')
            self.alerts.filter_by(region_type='marine', area='TX')
            self.alerts.filter_by(region_type='land', zone='CAZ054')
            self.alerts.filter_by(region_type='land', point='39,-99', region = 'AL')
            self.alerts.filter_by(region_type='marine', point='39,-99', area='TX')
            self.alerts.filter_by(region_type='marine', point='39,-99', zone='CAZ054')
            self.alerts.filter_by(region_type='land', point='39,-99', region='AL', area = 'TX')
            self.alerts.filter_by(region_type='land', point='39,-99', region='AL', zone = 'CAZ054')
            self.alerts.filter_by(region_type='land', point='39,-99', region='AL', area = 'TX', zone = 'CAZ054')

            # Point with all except above.
            self.alerts.filter_by(point='39,-99', region='AL')
            self.alerts.filter_by(point='39,-99', area='TX')
            self.alerts.filter_by(point='39,-99', zone='CAZ054')
            self.alerts.filter_by(point='39,-99', region='AL', area = 'TX')
            self.alerts.filter_by(point='39,-99', region='AL', zone ='CAZ054')
            self.alerts.filter_by(point='39,-99', region='AL', area = 'TX', zone = 'CAZ054')

            # Region with all except above.
            self.alerts.filter_by(region='AL', area='TX')
            self.alerts.filter_by(region='AL', zone='CAZ054')
            self.alerts.filter_by(region='AL', area='TX', zone='CAZ054')

            # area with zone
            self.alerts.filter_by(area='TX', zone='CAZ054')

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