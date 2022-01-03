import unittest
from old_package import nwsapy


class TestPoint(unittest.TestCase):

    def setUp(self):
        nwsapy.set_user_agent("NWSAPy Test - Points", "brandonmolyneaux@tornadotalk.com")
        self.point = nwsapy.get_point(33, -90)  # get info for this specific point.

    def test_check_attributes(self):
        attributes = ['cwa', 'forecastOffice', 'gridId', 'gridX', 'gridY', 'forecast', 'forecastHourly',
                      'forecastGridData', 'observationStations', 'city', 'state', 'distance', 'bearing',
                      'forecastZoneUrl', 'forecastZone', 'countyUrl', 'county', 'fireWeatherZoneUrl',
                      'fireWeatherZone', 'timeZone', 'radarStation']

        for attr in attributes:
            hasAttr = hasattr(self.point, attr)
            msg = f'Point does not have attribute {attr}.'
            self.assertTrue(hasAttr, msg=msg)

    def test_dtypes(self):
        attributes = {'cwa': str, 'forecastOffice': str, 'gridId': str, 'gridX': int, 'gridY': int,
                      'forecast': str, 'forecastHourly': str, 'forecastGridData': str, 'observationStations': str,
                      'city': str, 'state': str, 'distance': dict, 'bearing': dict, 'forecastZoneUrl': str,
                      'forecastZone': str, 'countyUrl': str, 'county': str, 'fireWeatherZoneUrl': str,
                      'fireWeatherZone': str, 'timeZone': str, 'radarStation': str}

        for attr in attributes:
            data_type = attributes[attr]
            self.assertTrue(isinstance(getattr(self.point, attr), data_type))
