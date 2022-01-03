Misc.
=====

Under the Hood
--------------
When using the package for your application, you're used to using
2 types of methods: ``set_user_agent`` and ``get_*``. However, you typically
don't touch the ``endpoints`` or ``services`` modules; this is because of 
how NWSAPy is designed. So this begs the question: how does NWSAPY work under 
the hood?

When you call a ``get_*`` method, first it checks to see if you've set the
user agent. Once this passes, it will do a data validation check. These are
simply lists and/or dictionaries mirroring the values found in the
:ref:`Data Validation Table` section.

Once this is complete, it will construct the URL based off of the arguments
that were passed into the ``get_*`` method. For example, 
``get_active_alerts(event = 'Severe Thunderstorm Warning')`` will construct a URL
that would be::
    
    https://api.weather.gov/alerts?event=Severe%20Thunderstorm%20Warning

Once this is created, then it requests the data from that URL and passes in
the data set with ``set_user_agent`` as header data, and then returns a response.
This response is parsed and placed into the respective endpoint object. Each
parsing is done differently based upon the object - it can be as simple as
setting the response json dictionary as the iterable object, or be much more
complicated.

Contributing
------------
See the :ref:`Contributing` guide.

Contact
-------
The easiest way to get in contact with the author is through Twitter: @WxBDM

Links
-----

All links open in a new tab.

- `GitHub <https://github.com/WxBDM/nwsapy>`_
- `Documentation <https://nwsapy.readthedocs.io/en/latest/>`_
- `National Weather Service API Documentation <https://www.weather.gov/documentation/services-web-api>`_
- `National Weather Service API <https://api.weather.gov/>`_
- `National Weather Service API Discussion <https://github.com/weather-gov/api/discussions>`_

Author Note
-----------
This is the first open source project I've made and consistently worked on.
This project means a lot to me, and I'm hoping that the weather community
and others outside of the weather community are able to use this to help
expidite the development process of their product, whether if it's a map
to be posted on Twitter or to be used in a larger application.

If you do use this, please let me know! I'm always open for feedback and comments, 
good or bad. I want to continue improving this package.

Google Documentation
--------------------

.. raw:: html
    :file: _static/google_doc_method_implementation.html

