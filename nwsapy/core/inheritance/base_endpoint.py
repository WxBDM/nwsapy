from warnings import warn

from nwsapy.core.inheritance.iterator import BaseIterator

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
    
    has_any_request_errors = False
    
    def __init__(self):
        super().__init__()
    
    # The following methods are pass-through methods. They'll get
    # "overwritten" (so to say) when they're defined in the child class.
    def to_df(self):
        """**Not implemented for this endpoint.**
        """
        msg = "to_df is not implemented for this endpoint. Returning `None`."
        warn(msg)
        return None

    def to_pint(self):
        """**Not implemented for this endpoint.**
        """
        msg = "to_pint is not implemented for this endpoint. Returning `None`."
        warn(msg)
        return None
    
    def to_dict(self):
        """**Not implemented for this endpoint.**
        """
        msg = "to_dict is not implemented for this endpoint. Returning `None`."
        warn(msg)
        return None