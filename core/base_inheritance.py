"""This file contains all base inheritance for NWSAPy."""

import pandas as pd
import json


class BaseBadRequest:
    """An object to be used when the request is bad."""

    def __init__(self, response):
        response = json.loads(response.text)
        for k, v in response.items():  # the response text is going to allow us to see the response from the API
            setattr(self, k, v)

        self._d = response

    def to_dict(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._d

    def to_dataframe(self):
        s = pd.Series(data = self._d)
        return pd.DataFrame(s).transpose() # transpose it so columns are named the attributes.

class AlertError(BaseBadRequest):
    def __init__(self, response):
        super().__init__(response)


class ErrorBase(Exception):
    """Passthrough class for handling custom-made errors."""

    pass


class ListIterator:
    """Allows objects in list-like format to be iterated over."""

    _iterable = None

    def set_iterable(self, iterable):
        """Sets the object to be iterated over."""

        self._iterable = iterable

    def _check_if_iterable_is_set(self):
        """Checks if the iterable object has been set or not."""

        if self._iterable is None:
            error_msg = "Iterable object has not been set. " \
                    "Please set it using self.set_iterable(iterable)"
            raise ValueError(error_msg)

    def __iter__(self):
        """Allows for iteration though object."""

        self._check_if_iterable_is_set()
        self._index = 0
        return self

    def __next__(self):
        """Allows for iteration through object."""

        self._check_if_iterable_is_set()
        if self._index < len(self._iterable):
            val = self._iterable[self._index]
            self._index += 1
            return val
        else:
            raise StopIteration

    def __getitem__(self, index):
        """Allows for object to be directly indexable."""
        self._check_if_iterable_is_set()
        return self._iterable[index]

    def __len__(self):
        self._check_if_iterable_is_set()
        return len(self._iterable)


# Is this even needed?
class DictionaryIterator:
    """A class to iterate over a dictionary structure."""


    # Utilities iterator only works for lists/tuples, not dictionaries.
    def __iter__(self):
        self._iterable = 0
        return self

    def __next__(self):
        if self._terms_index < len(self._iterable):
            val = self._iterable[self._terms_index]
            self._terms_index += 1
            return val
        else:
            raise StopIteration

    def __getitem__(self, term):
        return self._iterable[term]