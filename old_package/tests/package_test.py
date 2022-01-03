from old_package import nwsapy
from old_package.gridpoints import RawForecast
import old_package.utils as utils

nwsapy.set_user_agent("NWSAPy Benchmark Test", "brandonmolyneaux@tornadotalk.com")
alerts = nwsapy.get_raw_forecast('TOP', 31, 80)