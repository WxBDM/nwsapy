# This class allows us to iterate over both dictionaries and lists/tuples.
# A custom class is needed, as every endpoint.value is different - some
# are dictionaries (see: glossary), whereas some are lists (see: alerts).
# There isn't a python-builtin for iterating over both, so this "glues"
# the 2 types together.

# Note that when this is scaled, it could cause performance and/or memory issues.
# This would require re-writing to be optimized, but it's way above my head
# at the time of writing. For now though, this will do.

class BaseIterator:
    """Allows all NWSAPy objects to be iterable."""

    _iterable = None

    def _set_iterator(self, iterable):
        """Sets the object to be iterated over.
        
        If it's a dictionary, it'll set the keys as the iterable object.
        """
        
        if isinstance(iterable, dict):
            self._reference_to_dict = iterable
            self._type = 'dict'
            self._iterable = list(iterable.keys())
        else:
            self._type = 'list'
            self._iterable = iterable

    def _check_if_iterable_is_set(self):
        """Checks if the iterable object has been set or not.
        """
        if self._iterable is None:
            error_msg = "Iterable object has not been set. " \
                    "Please set it using self._set_iterator(iterable). " \
                    "If you see this message and you're not a developer, "\
                    "please open an issue on GitHub."
            raise ValueError(error_msg)

    def __len__(self):
        """Returns the length of the iterable object.
        """
        self._check_if_iterable_is_set()
        return len(self._iterable)
    
    def __iter__(self):
        """Allows for iteration though object.
        """
        self._check_if_iterable_is_set()
        self._index = 0
        return self

    def __next__(self):
        """Allows for iteration through object.
        """
        self._check_if_iterable_is_set()
        
        if self._index < len(self._iterable):
            val = self._iterable[self._index]
            self._index += 1
            
            if self._type == 'list':
                return val
            else:
                return (val, self._reference_to_dict[val])
        else:
            raise StopIteration

    def __getitem__(self, index_key):
        """Allows for object to be directly indexable.
        """
        self._check_if_iterable_is_set()
        if self._type == 'dict':
            return self._reference_to_dict[index_key]
        else:
            return self._iterable[index_key]

    def __len__(self):
        self._check_if_iterable_is_set()
        return len(self._iterable)
