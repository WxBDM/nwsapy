from warnings import warn
import pytest

from nwsapy.core.inheritance.iterator import BaseIterator
from nwsapy.core.request import request_from_api

# Every endpoint class will inherit this, it's inevitable. It's necessary to
#   create an abstract base endpoint class with a built-in iterator
#   with some pre-set values that will be used in every class.

# Remember: iterator does come with built-in checks to see if self._iterable
# has been set. If no iterator has been set, then it will throw an error
# using what is built into the language. Devs can set the iterator using 
# self._set_iterator(iter) in the __init__ function of the endpoint.
# Important note: be sure to use only lists as the iterable, it is not structured
# to handle dictionaries as of right now.
#   Note: this contains self._set_iterator() method.

# If any of the values (i.e. _DEPRECIATED) needs to be changed, don't change
# them here - change them in their respective child class.

# The majority of the classes will be structured as such:
#   __init__():
#       super().__init__()
#       response = self._request_api
#       # handle the class as appropriate
#       self._set_iterator(itr) <- This is relatively important. TODO: handle no iteration.

class BaseEndpoint(BaseIterator):
    
    # These aren't used for integrity checks, they're used in the base class.
    has_any_request_errors = False
    _DEPRECIATED = False
    
    # These are required variables, as they'll be checked using pytest.
    values = None
    _iterable = None    
    
    # These methods are implemented or not. it's a dev integreity check.
    _to_df_implement = None
    _to_pint_implement = None
    _to_dict_implement = None
    
    def __init__(self):
        
        if self._DEPRECIATED:
            msg = "This endpoint is depreciated. Please see the API specification"
            warn(msg)
        
    def _request_api(self, url, user_agent):
        
        # every endpoint requires a URL request.
        response = request_from_api(url, headers = user_agent)
        
        # check if it's an OK response. If not, set boolean to True.
        if not response.ok:
            self.has_any_request_errors = True
        
        # set the headers for every endpoint.
        self.response_headers = response.headers
        
        # It's going to be up to the dev to figure out how to organize and
        #   handle the response, so just return it.
        return response

    # The following methods are pass-through methods. They'll get
    # "overwritten" (so to say) when they're defined in the child class.
    def to_df(self):
        """Converts to a dataframe.
        """
        if not self._to_df_implement:
            msg = f"{__name__}.to_df() is not implemented. Nothing will be returned."
            warn(msg)
            return

    def to_pint(self):
        """Converts all units to pint.
        """
        if not self._to_df_implement:
            msg = f"{__name__}.to_pint() is not implemented. Nothing will be returned."
            warn(msg)
            return
    
    def to_dict(self):
        """Converts values to dictionaries.
        """
        if not self._to_df_implement:
            msg = f"{__name__}.to_dict() is not implemented. Nothing will be returned."
            warn(msg)
            return

    def _test_vals_have_been_set(self):
        """Test method to ensure that each endpoint has the necessary attributes.
        
        If you are using this for not NWSAPy development... please don't :^)
        
        """
        assert self.values == None
        assert self._iterable == None
    
    def _test_methods_have_been_set(self):
        """Test method to ensure that developers have set variables for 
        the implementation of the methods (to_xyz).
        """
        assert self._to_df_implement == None
        assert self._to_pint_implement == None
        assert self._to_dict_implement == None