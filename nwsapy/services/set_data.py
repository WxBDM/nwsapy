"""Sets the data for the object. For every one NWSAPy object, there is one
function to set the data. The data that is being set will sometimes differ,
so sometimes it'll just be setting the iterable and returning the object.
Some instances it'll set each value from the request as an attribute.
"""

from ..core.inheritance.request_error import RequestError

from ..endpoints.glossary import Glossary

def for_glossary(response):
    
    glossary = Glossary()
    
    if glossary.has_any_request_errors:
        values = RequestError(response)
    else:
        # iterate through the response and set the key/value pairs, then set
        # it into a `values` variable. This is then set into the glossary object.
        values = {}
        for element in response.json()['glossary']:
            values[element['term']] = element['definition']
    
    glossary.values = values
    glossary.response_headers = response.headers
    glossary._set_iterator_for_inherited_iterator()
    
    return glossary