
from old_package.errors import ParameterTypeError


class Point:

    def __init__(self, lat, lon):

        lat, lon = self._validate(lat, lon)
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f"Point object at {self.lat}, {self.lon}"

    def _validate(self, lat, lon):
        valid_lat = (isinstance(lat, int), isinstance(lat, float))
        valid_lon = (isinstance(lon, int), isinstance(lon, float))

        if not any(valid_lat):
            raise ParameterTypeError(lat, "int or float")
        if not any(valid_lon):
            raise ParameterTypeError(lon, "int or float")

        if isinstance(lat, int):
            lat = float(lat)
        if isinstance(lon, int):
            lon = float(lon)

        return round(lat), round(lon)


