
import nwsapy.utils as utils


class Glossary:

    def __init__(self, user_agent):
        response = utils.request("https://api.weather.gov/glossary", headers=user_agent)
        self.response_headers = response.headers  # requests.structures.CaseInsensitiveDict

        self.terms = {}
        for element in response.json()['glossary']:
            self.terms[element['term']] = element['definition']

        self._itr = list(self.terms.keys()) # make it iterable through keys list.

    def __iter__(self):
        """Allows for iteration though self.terms."""
        self._terms_index = 0
        return self

    def __next__(self):
        """Allows for iteration through self.alerts."""
        if self._terms_index < len(self._itr):
            val = self._itr[self._terms_index]
            self._terms_index += 1
            return val
        else:
            raise StopIteration

    def __getitem__(self, term):
        """Allows for alerts object to be directly indexable."""
        if isinstance(term, int): # if they're tyring to index like a list
            raise KeyError("Glossary not indexable, either iterate through it or")
        return self.terms[term]

