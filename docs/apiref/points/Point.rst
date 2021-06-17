Point
=====

.. currentmodule:: nwsapy

Introduction: Point
-------------------
To get a specific point by lat/lon values, use:

.. code-block:: python

    nwsapy.get_point(lat, lon)

This will return an ``Point`` object, as described in the API reference below.

The ``Point`` object is not iterable and indexable.

The methods that are implemented for :class:`Point` are::

    to_dict()
    to_pint()

It should be noted that the lat/lon is rounded to the closest 4 decimal places. This limitation is imposed by the API.

Example Usage: Point
--------------------
As of v0.2.0, you can only read in floats and integers. In a future version, you'll be able to read in a shapely point. But for now:

.. code-block:: python

    auburn = nwsapy.get_point(32.6099, -85.4808)

You can also read in a lat/lon more than 4 decimals, but it will be rounded to the nearest 4th decimal:

.. code-block:: python

    auburn = nwsapy.get_point(32.609900001, -85.4808000001)
    # This will round to 32.6099, -85.4808

If you wish to convert all the units using pint, pass in your unit registry:

.. code-block:: python

    from pint import UnitRegistry

    ureg = UnitRegistry()
    auburn = nwsapy.get_point(32.6099, -85.4808)
    auburn_to_pint = auburn.to_pint(ureg)

>>> print(auburn)
{'value': 73, 'unitCode': 'unit:degrees_true'}
>>> print(auburn_to_pint)
73 degree

API Reference: Point
--------------------

Method: get_point
^^^^^^^^^^^^^^^^^
.. automethod:: nwsapy.get_point

Class: points.Point
^^^^^^^^^^^^^^^^^^^

.. autoclass:: nwsapy.points.Point
    :inherited-members:
    :members:
