import unittest

from nwsapy.tests.alerts.individual_alerts import IndividualAlerts
from nwsapy.tests.alerts.filter_by import TestFilterBy


def test_scale_suite():
    scale_test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(IndividualAlerts),
        unittest.TestLoader().loadTestsFromTestCase(TestFilterBy),
    ])
    result = unittest.TestResult()
    runner = unittest.TextTestRunner()
    print(runner.run(scale_test_suite))


if __name__ == "__main__":
    test_scale_suite()