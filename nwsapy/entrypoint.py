"""Interface between the package and the user. All functionality is listed here
is for the user to call to interact with the Weather Service API.

There are some methods that take ``**kwargs`` as a parameter. For those not
familiar with this, this is short for "keyword arguments", for example::

    api_connector.get_all_alerts(event = "Severe Thunderstorm", )
                                 ^^^^^

This parameter is read in as ``{'event' : 'Severe Thunderstorm'}``, and is used
in the method. As such, the valid ``kwargs`` used in the method are listed
as "parameters" in this documentation in the respective method.
"""

# TODO: This. Fix it so it works!

# import datetime
# from typing import Union
# from warnings import warn

# needed: https://api.weather.gov/openapi.json

import requests
from warnings import warn
from requests import HTTPError

from .services.request import request_from_api

import nwsapy.services.set_data as set_data

from .endpoints.glossary import Glossary
from .endpoints.point import Point
from .endpoints.alerts import ActiveAlert

class ServerPing:
    """Sends a ping to the server.
    """
    def __init__(self, user_agent):
        response = request_from_api("https://api.weather.gov/", 
                                    headers=user_agent)
        self.values = response.json()['status']
        self.response_headers = response.headers
        

class NWSAPy:
    _app = None
    _contact = None
    _user_agent = None
    _user_agent_to_d = {'User-Agent': _user_agent}

    def _check_user_agent(self):
        if self._user_agent is None:
            msg = "Be sure to set the user agent before calling any " \
                "NWSAPy-related methods. To prevent this message from " \
                "appearing again, call `set_user_agent` method and set " \
                "your information as outlined in the documentation."
            warn(msg)

    def set_user_agent(self, app_name, contact):
        """Sets the User-Agent in header for requests. This should be unique to 
        your application.

        From the NWS API documentation: 
            "A User Agent is required to identify your application. This string 
            can be anything, and the more unique to your application the less 
            likely it will be affected by a security event. If you include 
            contact information (website or email), we can contact you if your
            string is associated to a security event."
        
        Link: https://www.weather.gov/documentation/services-web-api#/

        :param app_name: The name of your application.
        :type app_name: str
        :param contact: The contact email/website. This is needed for API 
            authentication.
        :type contact: str
        """
        self._app = app_name
        self._contact = contact
        self._user_agent = f"({self._app}, {contact})"
        self._user_agent_to_d = dict({'User-Agent': self._user_agent})
    
    def get_glossary(self):
        """Makes a request to the `/glossary` endpoint in the API and returns
        a glossary object containing information about the terms listed in
        the glossary.

        :return: An object containing information from the `/glossary` endpoint.
        :rtype: nwsapy.endpoints.glossary.Glossary
        """
        # check to make sure that the user agent is set.
        self._check_user_agent()
        
        # validate the parameters against DVT.
        # in this case, there aren't any params, so skip.

        # construct the URL (this case, hardcode it; it's static.)
        url = 'https://api.weather.gov/glossary'
        
        # make the request
        response = request_from_api(url, self._user_agent_to_d)
        
        # Set the data, return the nwsapy.endpoint.Glossary object.
        glossary = set_data.for_glossary(response)
      
        # return it.
        return glossary

    def get_point(self, lat, lon):
        """Makes a request to the `/point` endpoint in the API.
        
        This endpoint returns metadata about the given lat/lon.
        
        :return: An object containing information from the `/point` endpoint.
        :rtype: nwsapy.endpoints.point.Point
        """
        self._check_user_agent()
        return Point(lat, lon, self._user_agent_to_d)
    
    def ping_server(self):
        """Pings the server for integrity and/or testing.

        :return: ServerPing object
        :rtype: nwsapy.entrypoint.ServerPing
        """
        self._check_user_agent()
        return ServerPing(self._user_agent_to_d)

    def get_active_alerts(self, **kwargs):
        """[summary]

        :param area: The area in which the alert is in. Valid parameters are 
            typically the 2 letter abbreviation of the state in upper case 
            (i.e. "AL", "PA", etc)
        :type area: str or list[str]
        :param certainty: The certainty of the alert. Valid parameters: 
            "observed", "likely", "possible", "unlikely", "unknown"
        :type certainty: str or list[str]
        :param event: The type of alert (i.e. Severe Thunderstorm Warning, etc).
            Valid parameters are found on the data validation table.
        :type event: str or list[str]
        :param limit: The number of alerts to return at most. Will only retrieve
            the first n alerts.
        :type limit: int
        :param message_type: Either alert, update, or cancel.
        :type message_type: str or list[str]
        :param point: A tuple or list containing a latitude and longitude pair.
        :type point: list[float]
        :param region: A region where the alert resides. Valid data: AL, AT, GL, 
            GM, PA, or PI.
        :type region: str or list[str]
        :param region_type: The type of region where the alert resides. Valid
            data: land or marine.
        :type region_type: str
        :param severity: The severity level of the alert. Valid data: extreme,
            severe, moderate, minor, unknown
        :type severity: str or list[str]
        :param status: The status of the alert. Valid data: actual, exercise,
            system, test, draft
        :type status: str or list[str]
        :param urgency: The urgency of the alert. Valid data: unknown, past,
            future, expected, immediate
        :type urgency: str or list[str]
        :param zone: The NWS zone of the alert. Note this has no validation
            checks, so a 404 error can occur.
        :type zone: str or list[str]
        :return: An object containing information from the ``alerts/active``
            endpoint.
        :rtype: nwsapy.endpoints.alerts.ActiveAlert
        """
        
        self._check_user_agent()
        return ActiveAlert(self._user_agent_to_d, kwargs)