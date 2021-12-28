"""The inheritance core package allows the package to easily inherit
customized functionality for the core package. When developing, this should
not be touched unless a change is necessary. Due to the nature of inheritance,
any changes to existing functionality should be tested thoroughly before
merging into live code base.
"""

from . import iterator, request_error