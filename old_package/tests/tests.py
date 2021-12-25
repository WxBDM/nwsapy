import unittest

#from nwsapy.tests.alerts.individual_alerts import IndividualAlerts
from old_package.tests.alerts.filter_by import TestFilterBy
#from nwsapy.tests.points.test_point import TestPoint


def test_scale_suite():
    scale_test_suite = unittest.TestSuite([
        # unittest.TestLoader().loadTestsFromTestCase(IndividualAlerts),
        # unittest.TestLoader().loadTestsFromTestCase(TestFilterBy),
        #unittest.TestLoader().loadTestsFromTestCase(TestPoint),
    ])
    result = unittest.TestResult()
    runner = unittest.TextTestRunner()
    print(runner.run(scale_test_suite))


if __name__ == "__main__":
    test_scale_suite()
