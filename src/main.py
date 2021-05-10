
# Sample script of the UI that the user would have.

import nwsapi
import pprint

alert_by_id = nwsapi.get_alert_by_id("urn:oid:2.49.0.1.840.0.120d2da9a18007cad5170aeb93acff3abf04d935.001.1")
print(alert_by_id)