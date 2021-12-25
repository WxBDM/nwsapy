import math
import shapely.geometry as sg
from old_package.errors import ParameterTypeError


class Point:

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

        return values[0], values[1]





def check_point_type(pair):
    '''Checks if the data type (lat/lon) is correct.
    Expected: Int or Float.'''
    # data STRUCTURE checking
    # if it's a list, convert to tuple
    if isinstance(pair, list):
        pair = tuple(pair)
    # if it's anything else but a tuple, raise error.
    if type(pair) != tuple:
        raise TypeError("Lat/Lon pairs must be a tuple or list.")

    # length checking
    if len(pair) != 2:
        raise TypeError("Lat/Lon pairs need to be length of 2.")

    # data TYPE checking
    type_pairs = [pair[0], pair[1]]
    for i in [0, 1]:
        # if it's an int, change to float
        if isinstance(type_pairs[i], int):
            type_pairs[i] = float(type_pairs[i])
        # if it's anything else but a float, raise error.
        if not isinstance(type_pairs[i], float):
            raise TypeError("Ensure all pairs of lats/lons are ints or floats.")

    # Check if lat/lon falls within the proper range(s)
    # latitude: -90 to 90 inclusive
    # longitude: -180 to 180 inclusive
    if type_pairs[0] < -90.0 or type_pairs[0] > 90.0:
        raise TypeError("Latitude value must be -90 <= lat <= 90")
    if type_pairs[1] < -180 or type_pairs[0] > 180:
        raise TypeError("Longitude value must be -180 <= lon <= 180")

    return tuple(type_pairs)


def check_point_collection(collection):
    '''Checks to ensure the point collection is formatted correctly.'''

    # Check steps:
    # 1. If the outer structure is a list
    # 2. If there's at least 3 elements
    # 3. If all elements are a tuple (simply call check_point_type)

    # Step 1
    if not isinstance(collection, list):
        phrase = '''Collection must be a list. For example:
collection = [(9, 10), (2, 4), (3, 1), ...] where tuples are lat/lon pairs'''
        raise TypeError(phrase)

    # Step 2
    if len(collection) < 3:
        raise ValueError("Polygon must contain at least 3 lat/lon pairs")

    # Step 3
    # using enumerate here because there's a possibility that the tuple
    #   needs to get replaced; also allows to get the length
    new_collection = []
    for element in collection:
        pair = check_point_type(element)
        new_collection.append(pair)

    return [new_collection, len(collection)]


class Geometry:  # wrapper for shapely geometries

    def __init__(self, pynimbus_geometry):
        '''Sets the attributes to all PyNimbus Geometries'''
        self.area = pynimbus_geometry.area       # area
        self.bounds = pynimbus_geometry.bounds   # min/max of upper/lower/left/right
        self._geometry = pynimbus_geometry       # needed for below methods
        self.peek = pynimbus_geometry            # this is for UI purposes
        self.center = pynimbus_geometry.centroid.coords[0] # center of geometry

    def find_distance_to(self, other):
        '''Finds the distance between two PyNimbus Point geometry using the
        Haversine formula between two points. Note that this only calculates the
        distance between two points. Other PyNimbus Geometries such as lines
        and polygons shouldn't be used. Unexpected results may occur (and likely
        will).

        Parameters
        ----------
        other: `nhcoutlook.PyNimbus_Geometry`
        Returns
        -------
        distance: `float`
            Units: kilometers
        '''

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [self.lon, other.lon, self.lat, other.lat])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371 # Radius of earth in kilometers
        return c * r

    def contains(self, other):
        '''Determines if a PyNimbus geometry contains another geometry
        Parameters
        ----------
        other: `nhcoutlook.PyNimbus_Geometry`
        Returns
        -------
        boolean: `boolean`
        '''
        return self._geometry.contains(other._geometry)

    def crosses(self, other):
        '''Determines if 2 PyNimbus geometries cross eachother.
        Parameters
        ----------
        other: `nhcoutlook.PyNimbus_Geometry`
        Returns
        -------
        boolean: `boolean`
        '''
        return self._geometry.crosses(other._geometry)

    def is_disjointed_from(self, other):
        '''Determines if 2 PyNimbus geometries are disjointed
        Parameters
        ----------
        other: `nhcoutlook.PyNimbus_Geometry`
        Returns
        -------
        boolean: `boolean`
        '''
        return self._geometry.disjoint(other._geometry)

    def intersects_with(self, other):
        '''Determines if 2 geometries intersect eachother.

        Parameters
        ----------
        other: `nhcoutlook.PyNimbus_Geometry`
        Returns
        -------
        boolean: `boolean`
        '''
        return self._geometry.intersects(other._geometry)


class Point(Geometry):
    '''Class: PyNimbus Point.
    This class wraps a shapely Point and implements some of it's features.
    However, it applies specifically to PyNimbus's applications.
    This does not inheret the point collection class, as the features
    there are not needed.
    '''
    # This class creates a NimbusPoint - shapely.
    def __init__(self, lat_lon_pair):
        _pair = check_point_type(lat_lon_pair) # Data Checks
        self._point = sg.Point(_pair) # create the point using shapely
        super().__init__(self._point)

        # sets lat and lon of point.
        self.lat = self._point.__geo_interface__['coordinates'][0]
        self.lon = self._point.__geo_interface__['coordinates'][1]

    def __len__(self):
        return 2

    def __repr__(self):
        string = '''PyNimbus Point Geometry object.
    Latitude:  {0}
    Longitude: {1}
        '''.format(self.lat, self.lon)
        return string

    def get_coordinates(self):
        # Returns a tuple containing (lat, lon) pair.
        return tuple(self.lat, self.lon)


class _PointCollections(Geometry):

    def __len__(self):
        '''Returns the length of the geometry'''
        return self.length

    def __repr__(self):
        '''String representation'''
        if isinstance(self, Polygon):
            type_instance = 'Polygon'
        elif isinstance(self, Line):
            type_instance = 'Line'
        elif isinstance(self, ScatterPoints):
            type_instance = 'Scatter Points'

        phrase = '''PyNimbus {5} Geometry object.
    Number of Points: {0}
    Max Latitude:     {1}
    Max Longitude:    {2}
    Min Latitude:     {3}
    Min Longitude:    {4}'''.format(self.__len__(), self.bounds[0], self.bounds[1],
        self.bounds[2], self.bounds[3], type_instance)

        # without this, there is recursion. it eliminates this error.
        if type_instance != "Scatter Points":
            phrase += '''
    Center Point:     {}'''.format(self.center)

        return phrase

    def lats_to_list(self):
        '''Generates a list of latitudes'''
        return [coord[0] for coord in self.get_coords()]

    def lons_to_list(self):
        '''Generates a list of longitudes'''
        return [coord[1] for coord in self.get_coords()]

    def _get_collection(self, pair_list):
        '''Returns the collection of a list of pairs. Used in checking data types.
        Also sets the length of the collection to be used by __len__().'''

        info = check_point_collection(pair_list)
        self.length = info[1]
        return info[0]

    def get_coords(self):
        '''Returns the paired coordinates for a given PyNimbus geometry.'''

        if isinstance(self, Polygon):
            return list(self._polygon.__geo_interface__['coordinates'][0])
        elif isinstance(self, Line) or isinstance(self, ScatterPoints):
            return list(self._polygon.__geo_interface__['coordinates'])

        return None # in case it's not any of these; unlikely to happen. Failsafe.

    def lat_lon_to_plot(self):
        '''Prepares the latitudes and longitudes to be easily plotted
        using a mapping package such as Cartopy.'''
        if isinstance(self, Polygon):
            x = list(self._polygon.exterior.xy[0])
            y = list(self._polygon.exterior.xy[1])
            return [x, y]
        elif isinstance(self, Line):
            x = list(self._polygon.xy[0])
            y = list(self._polygon.xy[1])
            return [x, y]
        elif isinstance(self, ScatterPoints):
            x = [p.x for p in self._polygon.geoms]
            y = [p.y for p in self._polygon.geoms]
            return [x, y]

class Polygon(_PointCollections):
    # this class creates a NimbusPolygon - Shapely Polygon
    '''Class: PyNimbus Polygon.
    This class wraps a shapely Polygon and implements some of it's features.
    However, it applies specifically to PyNimbus's applications.
    '''

    def __init__(self, lat_lon_pair_list):
        # collection returns the "corrected" collection and the length of it.
        self.__collection = super()._get_collection(lat_lon_pair_list)
        self._polygon = sg.Polygon(self.__collection) # the shapely polygon
        self.coords = super().get_coords()
        super().__init__(self._polygon)

class Line(_PointCollections):
    # this class creates a NimbusLine - Shapely Line
    '''Class: PyNimbus Line.
    This class wraps a shapely Line and implements some of it's features.
    However, it applies specifically to PyNimbus's applications.
    '''

    def __init__(self, lat_lon_pair_list):
         # collection returns the "corrected" collection and the length of it.
        self.__collection = super()._get_collection(lat_lon_pair_list)
        self._polygon = sg.LineString(self.__collection) # the shapely polygon
        self.coords = super().get_coords()
        super().__init__(self._polygon)

class ScatterPoints(_PointCollections):
    '''Class: PyNimbus Scatter Points.
    This class wraps a shapely MultiPoint and implements some of it's features.
    However, it applies specifically to PyNimbus's applications.
    '''
    # collection returns the "corrected" collection and the length of it.
    def __init__(self, lat_lon_pair_list):
        self.__collection = super()._get_collection(lat_lon_pair_list)
        self._polygon = sg.MultiPoint(self.__collection) # the shapely polygon
        self.coords = super().get_coords()
        super().__init__(self._polygon)
