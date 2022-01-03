import pandas as pd

from nwsapy.core.inheritance.base_endpoint import BaseEndpoint

class Glossary(BaseEndpoint):
    
    def __init__(self):
        
        # initialize the BaseEndpoint __init__ class.
        super(Glossary, self).__init__()
    
    def to_dict(self):
        """Returns the glossary in a dictionary format.

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