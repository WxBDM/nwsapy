from nwsapy.core.inheritance.request_error import RequestError
from nwsapy.core.inheritance.base_endpoint import BaseEndpoint

class Template(BaseEndpoint):
    
    # Copy/Paste these values for each base method that is a "passthrough".
    _to_df_implement = False
    _to_pint_implement = False
    _to_dict_implement = False
    
    def __init__(self, user_agent):
        super(BaseEndpoint, self).__init__()
        
        url = 'change_me'
        response = self._request_api(url, user_agent)
        
        if self.has_any_request_errors:
            self.values = RequestError(response)
        else:
            self.values = 'CHANGE ME BECAUSE IT WILL VARY ACROSS ENDPOINTS'
        
        self._set_iterator(self.values)