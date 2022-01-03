Introduction to NWSAPy
======================

.. toctree::
    :maxdepth: 1

    Endpoints Dashboard <endpoints>
    API Reference <api_ref/api_ref>

Some key things to know
-----------------------
- NWSAPy does *not* handle fetching data in the NWS servers. 
  That is, it only interfaces with the National Weather Service API, and their 
  API handles ``GET`` requests for their server.
- All data from the NWS API is done through ``get_*(kwargs)`` functions.
  For example, ``get_active_alerts(event = "Tornado Warning")`` will get
  all active Tornado warnings.
- Not all endpoints are currently implemented. See the 
  :ref:`Endpoints Dashboard <Endpoints Dashboard>` to see what is currently
  implemented.
- When passing in parameters to ``nwsapy`` methods (see: second point in this
  section for an example), ensure that it is spelled *exactly* the same way,
  including upper case and lower case methods. These values can be found
  in their respective :ref:`Data Validation Tables <dvt>`.

An Example, Explained
---------------------
NWSAPy is designed to be a simple, yet pythonic way to interface with the
National Weather Service API. This section outlines how to use NWSAPy, generally
speaking, for your application by stepping through a simple example. More details
for each individual ``get_*(kwargs)`` method can be found in their respective
documentation areas.

Starting with a simple example:

.. code-block:: python

    from nwsapy import api_connector

    api_connector.set_user_agent('Application Name', 'Contact information')
    server_ping = api_connector.ping_server()

This will print ``OK`` if the request was successful. Breaking it down::

    from nwsapy import api_connector

``api_connector`` is the object that's being used to interface with the package.
That is, all methods that are called are encapsulated in ``api_connector``.

.. note::
    For those who have used NWSAPy before v1.0.0, this was originally
    ``from nwsapy import nwsapy``. You are still able to do this, but this will
    be removed in a future version.

The next line is ``set_user_agent``::

    api_connector.set_user_agent('Application Name', 'Contact Information')

The user agent gets put into the header information when making a request. This
is a field that the maintainers of the National Weather Service API would like
to have in case your request is associated with a security event. ``Application
Name`` should be unique to your application, and ``Contact Information`` can be
a website or an email. Without this line, NWSAPy will warn you and let you know 
that you should use this when making any kind of request to the National Weather
Service API.

.. important::
    NWSAPy does *not* store the information to be used outside of making a request
    to the National Weather Sevice API. This information is passed into a method
    in the ``requests`` module (specifically, ``requests.get()``).

Following this::

    server_ping = api_connector.ping_server()

This pings the server and returns an object that you are able to utilize.
In this case, it is a ``nwsapy.endpoints.server_ping.ServerPing`` object.
See the documentation on :class:`ServerPing` to see the attributes of
the ``ServerPing`` object obtained from :meth:`get_server_ping`.

this is where NWSAPy is able to be leveraged for your project: it organizes
all of the data coming from the Natoinal Weather Service API in a pythonic manner
through ``get_*(kwargs)`` methods. It also keeps code that you create using
this package clean and straight-forward.

For instance, if we were to iterate through the ``ServerPing`` object:

.. code-block:: python

    for key, value in server_ping:
        print(f'Key: {key}, Value: {value}')

We would see::

    Key: status, Value: OK

Under the hood (in this instance), it's iterating through a dictionary. There
are some objects that have a list under the hood that it is iterating through.
Details of this can be found in the respective ``get_*(kwargs)`` method.
