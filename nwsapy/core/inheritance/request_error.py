import json
import pandas as pd

# The docs on this look weird, fix.
class RequestError:
    """An object to be used when the request is bad.\n
    Attributes:
    
        type
            A URI reference (RFC3986) that identifes the problem type.\n
        title
            A short, human-readable summary of the problem type.\n
        status
            The HTTP status code (RFC7231, Section 6) generated by the origin server 
            for this occurrence of the problem. 
            Minimum: 100, Max 999\n
        detail
            A human-readable explaination specific to this occurance of the problem.\n
        instance
            A URI reference that identifies the specific occurence of the problem.\n
        correlationId
            A unique identifier for the request, used for NWS debugging purposes.
            Please include this identifier with any correspondence to help the API 
            maintainers investigate your issue.
    """

    def __init__(self, response):
        """Constructor to unpack json-formatted response and set them
        as attributes to this class.
        """
        response = json.loads(response.text)
        # the response text is going to allow us to see the response from the API
        for k, v in response.items(): # set each 
            setattr(self, k, v)

        self.values = response

    def to_dict(self):
        """Returns a dictionary of the associated error object.

        :return: dictionary containing response details.
        :rtype: dictionary
        """
        return self.values

    def to_df(self):
        """Formats the error object response in a Pandas dataframe, with
        columns are the attributes.

        :return: Dataframe
        :rtype: pd.DataFrame
        """
        s = pd.Series(data = self.values)
        return pd.DataFrame(s).transpose() # transpose it so columns are named the attributes.