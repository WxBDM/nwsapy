"""Interface between the package and the user. All functionality is listed here
is for the user to call to interact with the Weather Service API.
"""

# TODO: This. Fix it so it works!

# import datetime
# from typing import Union
# from warnings import warn

# needed: https://api.weather.gov/openapi.json

from warnings import warn

from .core.request import request_from_api

class ServerPing:
    """Tests the server to make sure it's OK."""

    def __init__(self, user_agent):
        response = request_from_api("https://api.weather.gov/", headers=user_agent)
        self.status = response.json()['status']
        self.response_headers = response.headers
        

class NWSAPy:
    _app = None
    _contact = None
    _user_agent = None
    _user_agent_to_d = {'User-Agent': _user_agent}

    def _check_user_agent(self):
        if self._user_agent is None:
            warn(f"Be sure to set the user agent before calling any nwsapy functions. To prevent this message from "
                  f"appearing again, use: nwsapy.set_user_agent(app_name, email/website)")

    def set_user_agent(self, app_name, contact):
        """Sets the User-Agent in header for requests. This should be unique to your application.

        From the NWS API documentation: "A User Agent is required to identify your application.
        This string can be anything, and the more unique to your application the less likely it will be
        affected by a security event. If you include contact information (website or email), we can contact
        you if your string is associated to a security event."
        (Link: https://www.weather.gov/documentation/services-web-api#/)

        Parameters
        ----------
        app_name : str
            The name of your application.
        contact : str
            The contact email. This is needed for API authentication.

        """

        # # check data types
        # if not isinstance(app_name, str):
        #     raise ParameterTypeError(app_name, str)
        # if not isinstance(contact, str):
        #     raise ParameterTypeError(contact, str)

        self._app = app_name
        self._contact = contact
        self._user_agent = f"({self._app}, {contact})"
        self._user_agent_to_d = dict({'User-Agent': self._user_agent})
        
    def ping_server(self):
        """Pings https://api.weather.gov/ to see status

        Returns
        -------
        :class:`utils.ServerPing`
        """
        self._check_user_agent()
        return ServerPing(self._user_agent_to_d)