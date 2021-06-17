# NWS-APy: A Pythonic Implementation of the National Weather Service API

NWS-APy (APy for short) takes a pythonic approach to retrieving (GET) and organizing data using the National Weather Service API (found here: https://www.weather.gov/documentation/services-web-api#/)

There are 3 goals that the package aims to achieve:
- Keep clean, simplistic, minimalistic, and consistent code on the user end.
- Minimize potential 404/500 errors and knowledge overhead.
- Format output to popular meteorological data types.

## A simple example

APy is designed to be simple and easy to use. For example, if we wanted to get all of the tornado warnings in Oklahoma and just display the headline:

```python
from nwsapy import nwsapy

tor_warnings_in_ok = nwsapy.get_active_alerts(event = "Tornado Warning", area = "OK")
for warning in tor_warnings_in_ok:
    print(warning.headline)
```

## Documentation

Documentation for NWSAPy be found [here](https://nwsapy.readthedocs.io/en/latest/index.html)

## Contact/Support

I want to hear from you. If you have any questions regarding the package usage, please [send me an email](mailto:brandonmolyneaux@tornadotalk.com). If you encounter an issue, please open an issue on GitHub.
