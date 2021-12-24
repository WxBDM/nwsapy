from nwsapy_old import nwsapy
from nwsapy_old.gridpoints import RawForecast
import nwsapy_old.utils as utils

nwsapy.set_user_agent("NWSAPy Benchmark Test", "brandonmolyneaux@tornadotalk.com")
alerts = nwsapy.get_raw_forecast('TOP', 31, 80)