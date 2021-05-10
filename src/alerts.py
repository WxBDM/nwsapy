import collections
from dataclasses import dataclass

from shapely.geometry import Point, Polygon, MultiPoint

import utils


@dataclass
class Alert:
    # Base class for alerts sub classes.

    @staticmethod
    def _sort_geometry(alert_list):
        # determine the geometry kind. If it's a point, make a list of shapely point objects, and create a multipoint
        # object.
        if isinstance(alert_list['geometry'], type(None)):  # if there's no geometry (i.e. 'geometry' : null)
            d = dict(points=None, polygon=None, points_collection=None)  # set to none. This is to remain to consistent
        else:
            # If there is a geometry, then make points and points collection at a minimum.
            geometry_type = alert_list['geometry']['type']
            d = {}
            points = [Point(x[0], x[1]) for x in alert_list['geometry']['coordinates'][0]]
            points_collection = MultiPoint(points)
            d['points'] = points
            d['points_collection'] = points_collection

            # If the geometry type is a polygon, make a polygon object as well. Otherwise set to none.
            if geometry_type == 'Polygon':
                d['polygon'] = Polygon(points)
            else:
                d['polygon'] = None

        # properties is a nested dictionary. Need to create a new dictionary and then update it with logic from above.
        full_d = alert_list['properties']
        full_d.update(d)

        # this will be the object that's created based on the event.
        #    for example, if it was a tornado warning, the object would be "tornadowarning"
        alert = type(full_d['event'].replace(" ", "").lower(), (), full_d)
        return alert()  # this instantiates the object. Don't change this!

    def get_number_of(self, alert_type):
        """A method to give you the number of alerts of a specific type that are active.

        For example, if you wanted to see the number of flood warnings:
            get_number_of_alerts_of_type("Flood Warning")
        This would return a number (integer).

        Parameters
        ==========
            alert_type (str): The type of alert to be searched. Not case sensitive.

        Returns
        =======
            number_of_alerts (int): The number of alerts that are of the alert type.
        """

        # data checking.
        if not isinstance(alert_type, str):
            raise ValueError("The alert type must be a string.")

        # make sure it's a valid product. If so, then we're okay to check inside of the collections.
        alert_type = alert_type.title()
        valid_product_link = "https://api.weather.gov/alerts/types"
        response = utils.request(valid_product_link)
        event_types = response.json()['eventTypes']
        if alert_type not in event_types:
            raise ValueError(f"{alert_type} not found in valid products. Check spelling.")

        # valid data type, valid product. Get it from counter. (O(1))
        if alert_type not in self.counter:
            return 0
        else:
            return self.counter[alert_type]


@dataclass
class ActiveAlerts(Alert):

    def __init__(self, response):
        info = response.json()['features']
        self.all_alerts = [self._sort_geometry(x) for x in info]  # opted for list comp because it's faster
        self.counter = collections.Counter(x.event for x in self.all_alerts)  # counts the number of alerts

@dataclass
class AlertById(Alert):

    def __init__(self, alert_id):
        response = utils.request(f"https://api.weather.gov/alerts/{alert_id}")
        info = response.json()
        print(info)
