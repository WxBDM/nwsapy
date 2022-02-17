from warnings import warn
import copy
import pint

from nwsapy.core.inheritance.base_endpoint import BaseEndpoint

class Point(BaseEndpoint):
    

    def __init__(self):
        super(Point, self).__init__()

    def to_dict(self) -> dict:        
        """Returns a dictionary with all of the attributes to the class.

        :return: Dictionary of the attributes of the class.
        :rtype: dictionary
        """
        return self.values

    def to_pint(self, unit_registry : pint.UnitRegistry) -> object:
        """Returns a new self object with units using Pint. It does NOT update
        in-place.

        :param unit_registry: Your unit registry used in your application.
        :type unit_registry: pint.UnitRegistry
        :return: Dictionary with values converted to pint units.
        :rtype: dictionary
        """

        # Need to create a deep copy, behavior of dictionaries are different
        #   than lists, they don't create a copy of themselves
        new_point_obj = copy.deepcopy(self)
        
        # check each attribute, then create
        if hasattr(self, 'distance'):
            distance = self.distance['value'] * unit_registry.meter
            new_point_obj.distance = distance
            new_point_obj.series['distance'] = distance
        if hasattr(self, 'stations'):
            for station in self.stations:
                station_elevation = station.elevation['value'] * unit_registry.meter
                station.elevation = station_elevation
                station.series['elevation'] = station_elevation
        if hasattr(self, 'bearing'):
            bearing = self.bearing['value'] * unit_registry.degrees
            new_point_obj.bearing = bearing
            new_point_obj.series['bearing'] = bearing

        return new_point_obj