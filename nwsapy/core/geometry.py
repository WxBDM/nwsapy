"""Houses the geometry NWSAPy uses internally. This is a wrapper for the
shapely library with select functionality to be used for NWSAPy.
"""

import shapely.geometry as sg


class Point:
    """Point object.
    
    :param lat: The latitude of the point.
    :type lat: integer or float
    :param lon: The longitude of the point.
    :type lon: integer or float
    """
    def __init__(self, lat, lon):
        lat, lon = self._validate(lat, lon)
        self.latitude = lat
        self.longitude = lon

    def __len__(self):
        return 2

    def __repr__(self):
        string = f'NWSAPy Point Geometry object. Latitude: {self.latitude} Longitude: {self.longitude}'
        return string

    def _validate(self, lat, lon):
        # checks the points and ensures they're float/int. Convert to float and truncate to 4 decimal places.
        values = [lat, lon]

        for index, val in enumerate(values):
            valid = (isinstance(val, int), isinstance(val, float))

            if not any(valid):
                raise ValueError(f"Value: {val} is not float/int. Got: {type(val)}")

            values[index] = float(format(val, ".4f"))
            
            # There's a better way to write this.
            # if it's latitude, check to see if it's between -90 and 90.
            if index == 0:
                if any([val > 90, val < -90]):
                    raise ValueError(f"Latitude must be between -90 and 90. Found: {val}.")
            # if it's longitude, check to see if it's between -180 and 180.
            if index == 1:
                if any([val > 180, val < -180]):
                    raise ValueError(f"Longitude must be between -180 and 180. Found: {val}")

        return values[0], values[1]