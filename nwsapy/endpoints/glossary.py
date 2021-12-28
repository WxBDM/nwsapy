import pandas as pd

from nwsapy.core.inheritance.request_error import RequestError
from nwsapy.core.inheritance.base_endpoint import BaseEndpoint

class Glossary(BaseEndpoint):
    
    def __init__(self):
        
        # initialize the BaseEndpoint __init__ class.
        super(Glossary, self).__init__()
        
        # TODO: delete once testing has been done.
        
        # # make the request to the API.
        # response = self._request_api("https://api.weather.gov/glossary",
        #                             user_agent)
        
        # # handle the response appropriately specific to this class.
        # if self.has_any_request_errors:
        #     self.values = RequestError(response)
        # else:
        #     self.values = {}
        #     for element in response.json()['glossary']:
        #         self.values[element['term']] = element['definition'] 
        
        # # set the iterable
        # self._set_iterator(self.values)
    
    def to_dict(self):
        """Returns a dictionary

        :return: Dictionary containing the values of the glossary.
        :rtype: dict
        """
        return self.values

    def to_df(self):
        """Returns the values of the glossary in a pandas dataframe structure.

        :return: Dataframe of the values of the glossary.
        :rtype: pandas.DataFrame
        """
        data = {'Term' : list(self.values.keys()),
                'Definition' : list(self.values.values())}
        return pd.DataFrame.from_dict(data)