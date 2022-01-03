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

from warnings import warn

from nwsapy.core.mapping import full_state_to_two_letter_abbreviation

from .services.validation import DataValidationChecker
from .services.url_constructor import construct_alert_url
from .services.request import request_from_api
import nwsapy.services.set_data as set_data



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
    
    def make_request(self, url):
        """Makes a request to the NWS API with a given URL. This method allows
        you to have full control over the data without the functionality
        and organization of any NWSAPy ``get_*`` methods.
        
        .. note::
            This does not have any kind of data validation checks and 
            does not handle any errors on behalf of you.

        :param url: The URL to make a request to the NWS API.
        :type url: string
        :return: A response object containing the request for the query.
        :rtype: request.Response
        """
        self._check_user_agent()
        response = request_from_api(url, self._user_agent_to_d,                 as_response_object = True)
    
        return response
    
    def get_glossary(self):
        """Makes a request to the `/glossary` endpoint in the API and returns
        a glossary object containing information about the terms listed in
        the glossary.
        
        | Endpoint: ``/glossary``  
        | Description: Glossary terms

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
        """Makes a request to the `/point` endpoint in the API and returns
        a point object containing metadata about the given lat/lon.
        
        | Endpoint: ``/points/{point}``  
        | Description: Returns metadata about a given latitude/longitude point.
                
        :return: An object containing information from the `/point` endpoint.
        :rtype: nwsapy.endpoints.point.Point
        """
        self._check_user_agent()
        
        # validate the data
        dvt = DataValidationChecker()
        dvt.check_lat_lon(lat, lon)
        
        # Construct the URL
        url = f'https://api.weather.gov/points/{lat}%2C{lon}'
        
        # Make the request
        response_tuple = request_from_api(url, self._user_agent_to_d)
        
        # Set the data
        point = set_data.for_point(response_tuple)
        
        return point
    
    def ping_server(self):
        """Pings the server for integrity and/or testing.

        :return: ServerPing object
        :rtype: nwsapy.entrypoint.ServerPing
        """
        self._check_user_agent()
        url = 'https://api.weather.gov'
        response_tuple = request_from_api(url, self._user_agent_to_d)
        ping = set_data.for_server_ping(response_tuple)
        return ping
    
    def get_active_alerts(self, **kwargs):
        """Returns an active alerts object containing all active alerts. This
        object is comprised of :ref:`IndividualAlerts`.
        
        | Endpoint: ``/alerts/active``  
        | Description: Returns all currently active alerts.
        
        :param area: The land or marine region where the alert is in. Either a 2
            letter abbreviation (i.e. "FL") or the full state name (i.e. "Florida")
            :ref:`Data Validation Table <Area DVT>`
        :type area: str or list[str]
        :param certainty: The certainty of the alert. :ref:`Data Validation Table <Certainty DVT>`
        :type certainty: str or list[str]
        :param event: The type of alert (i.e. Severe Thunderstorm Warning, etc).
            :ref:`Data Validation Table <Product DVT>`
        :type event: str or list[str]
        :param limit: The number of alerts to return at most. Will only retrieve
            the first n alerts.
        :type limit: int
        :param message_type: :ref:`Data Validation Table <Message Types DVT>`
        :type message_type: str or list[str]
        :param point: A tuple or list containing a latitude and longitude pair.
        :type point: list[float]
        :param region: A marine region where the alert resides. 
            :ref:`Data Validation Table <Marine DVT>`
        :type region: str or list[str]
        :param region_type: The type of region where the alert resides.
            :ref:`Data Validation Table <Region Type DVT>`
        :type region_type: str
        :param severity: The severity level of the alert. 
            :ref:`Data Validation Table <Severity DVT>`
        :type severity: str or list[str]
        :param status: The status of the alert. 
            :ref:`Data Validation Table <Status DVT>`
        :type status: str or list[str]
        :param urgency: The urgency of the alert. 
            :ref:`Data Validation Table <Urgency DVT>`
        :type urgency: str or list[str]
        :param zone: The NWS zone of the alert. Note this has no validation
            checks, so a 404 error can occur.
        :type zone: str or list[str]
        :return: An object containing information from the ``alerts/active``
            endpoint.
        :rtype: nwsapy.endpoints.alerts.ActiveAlert
        """
        self._check_user_agent() # header
        dvt = DataValidationChecker() # insantiate dvt
        dvt.check_active_alerts_dvt(kwargs) # validate the kwargs
        url = construct_alert_url(kwargs) # construct url
        response_tuple = request_from_api(url, self._user_agent_to_d) # get data
        active_alerts = set_data.for_active_alerts(response_tuple) # get alert object
        return active_alerts # give back to user

    def get_alerts(self, **kwargs):
        """Returns an alerts object with the previous 500 alerts. Note that
        this is the maximum value and also the default.
        
        | Endpoint: ``/alerts``  
        | Description: Returns all alerts.
        
        :param area: The land or marine region where the alert is in. Either a 2
            letter abbreviation (i.e. "FL") or the full state name (i.e. "Florida")
            :ref:`Data Validation Table <Area DVT>`
        :type area: str or list[str]
        :param certainty: The certainty of the alert. :ref:`Data Validation Table <Certainty DVT>`
        :type certainty: str or list[str]
        :param event: The type of alert (i.e. Severe Thunderstorm Warning, etc).
            :ref:`Data Validation Table <Product DVT>`
        :type event: str or list[str]
        :param limit: The number of alerts to return at most. Will only retrieve
            the first n alerts.
        :type limit: int
        :param message_type: :ref:`Data Validation Table <Message Types DVT>`
        :type message_type: str or list[str]
        :param point: A tuple or list containing a latitude and longitude pair.
        :type point: list[float]
        :param region: A marine region where the alert resides. 
            :ref:`Data Validation Table <Marine DVT>`
        :type region: str or list[str]
        :param region_type: The type of region where the alert resides.
            :ref:`Data Validation Table <Region Type DVT>`
        :type region_type: str
        :param severity: The severity level of the alert. 
            :ref:`Data Validation Table <Severity DVT>`
        :type severity: str or list[str]
        :param status: The status of the alert. 
            :ref:`Data Validation Table <Status DVT>`
        :type status: str or list[str]
        :param urgency: The urgency of the alert. 
            :ref:`Data Validation Table <Urgency DVT>`
        :type urgency: str or list[str]
        :param zone: The NWS zone of the alert. Note this has no validation
            checks, so a 404 error can occur.
        :type zone: str or list[str]
        :return: An object containing information from the ``alerts/active``
            endpoint.
        :rtype: nwsapy.endpoints.alerts.ActiveAlert
        """
        
        # TODO: handle start/end times. need to investigate inputs and how
        #   to translate from datetime object to what API accepts.
        #   maybe also put it in data validation table?
        
        self._check_user_agent() # header
        dvt = DataValidationChecker() # insantiate dvt
        dvt.check_active_alerts_dvt(kwargs) # validate the kwargs
        url = construct_alert_url(kwargs, is_active_alerts = False) # construct url
        response_tuple = request_from_api(url, self._user_agent_to_d) # get data
        active_alerts = set_data.for_active_alerts(response_tuple) # get alert object
        return active_alerts # give back to user

    def get_alert_by_id(self, id):
        """Retrieves an alert by ID from the ``alerts/active/{id}`` endpoint.
        
        | Endpoint: ``alerts/active/{id}``  
        | Description: Returns a specific alert

        :param id: The ID of an alert.
        :type id: string
        :return: An object containing information about the specified alert.
        :rtype: nwsapy.endpoints.alerts.AlertById
        """
        
        self._check_user_agent()
        url = f'https://api.weather.gov/alerts/{id}'
        response_tuple = request_from_api(url, self._user_agent_to_d)
        alert_by_id = set_data.for_alert_by_id(response_tuple)
        return alert_by_id

    def get_alert_by_area(self, area):
        """Retrieves alerts by a given area (state or marine).
        
        | Endpoint: ``alerts/active/area/{area}``  
        | Description: Retrieves alerts for the given area (state or marine area)

        :param area: 2 letter state abbreviation or full state name (i.e. Florida)
            :ref:`Data Validation Table <Area DVT>`
        :type area: str
        :return: An object containing information about the specified alert.
        :rtype: nwsapy.endpoints.alerts.AlertByArea
        """
        
        self._check_user_agent()
        dvt = DataValidationChecker()
        dvt.check_if_valid_area(area)
        
        # in the event it's not a 2 letter abbreviation, convert it.
        # Guarenteed to be in there, as data validation happened already.
        if len(area) != 2:
            area = full_state_to_two_letter_abbreviation(area)
        
        url = f'https://api.weather.gov/alerts/active/area/{area}'
        response_tuple = request_from_api(url, self._user_agent_to_d)
        alert_by_area = set_data.for_alert_by_area(response_tuple)
        return alert_by_area

    def get_alert_by_zone(self, zone):
        """Retrieves alerts by the 6 character NWS zone or county. Note that this
        method does *not* have any data validation checks as of v1.0.0.

        | Endpoint: ``/alerts/active/zone/{zoneId}``  
        | Description: Returns active alerts for the given NWS public zone or county

        :param zone: A 6 character NWS zone or county (ex: BAC222)
        :type zone: str
        :return: An object containing information about the NWS public zone or county
        :rtype: nwsapy.endpoints.alerts.AlertByZone
        """
        
        self._check_user_agent()
        # There needs to be a data validation table for this. Something for someone
        # to contribute to.
        url = f"https://api.weather.gov/alerts/active/zone/{zone}"
        response_tuple = request_from_api(url, self._user_agent_to_d)
        alert_by_zone = set_data.for_alert_by_zone(response_tuple)
        return alert_by_zone
    
    def get_alert_by_marine_region(self, marine_region):
        """Retrieves alerts by a specific marine region.
        
        | Endpoint: ``alerts/active/region/{regionId}``  
        | Description: Returns active alerts for the given marine region

        :param marine_region: A 2 letter marine region.
            :ref:`Data Validation Table <Marine DVT>`
        :type marine_region: str
        :return: An object containing information about alerts in the specified marine region.
        :rtype: nwsapy.endpoints.alerts.AlertByRegion
        """
        
        self._check_user_agent()
        dvt = DataValidationChecker()
        dvt.check_if_valid_marine_region(marine_region)
        url = f"https://api.weather.gov/alerts/active/region/{marine_region}"
        # TODO: add into core mapping the marine regions.
        # TODO: Data validation check: lowercase to uppercase. validator doesn't handle.
        response_tuple = request_from_api(url, self._user_agent_to_d)
        alert = set_data.for_alert_by_marine_region(response_tuple)
        return alert
        
    def get_alert_count(self):
        """Gets the number of land, marine, and total active alerts. Also
        provides a dictionary of the number of alerts by areas (states),
        zones, and marine regions.
        
        Endpoint: ``/alerts/active/count``  
        Description: Returns info on the number of active alerts.

        :return: An object containing the number of alerts for certain parameters.
        :rtype: nwsapy.endpoints.alerts.AlertCount
        """
        self._check_user_agent()
        url = "https://api.weather.gov/alerts/active/count"
        response_tuple = request_from_api(url, self._user_agent_to_d)
        alert_count = set_data.for_alert_count(response_tuple)
        return alert_count

    def get_alert_types(self):
        """Retrieves a list of the alert types that the National Weather 
        Service puts out.
        
        Endpoint: ``/alerts/types``  
        Description: Returns a list of alert types.
        
        .. note::

            NWSAPy has this built in as a data validation table. To retrieve:
            
            .. code-block:: python

                from nwsapy.services.validation import valid_products
                products = valid_products()
            
            Using this will allow for your code to be run quicker, as it
            retrieves a list compared to a NWS API request.
            

        :return: An object containing information about the alert types.
        :rtype: nwsapy.endpoints.alert.AlertType
        """
        self._check_user_agent()
        url = 'https://api.weather.gov/alerts/types'
        response_tuple = request_from_api(url, self._user_agent_to_d)
        types = set_data.for_alert_type(response_tuple)
        return types