"""The core package can be thought of as a package with static-like objects
and functionalities that are done at the low level, such as mapping
between state names, constructing base objects, and base inheritance
objects; think of it as the "base" of the entire project.

Any changes to this module should be reviewed carefully, as any changes
could break the code. Services and endpoints use this package to define
base-like objects.
"""