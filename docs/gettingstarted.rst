===============
Getting Started
===============

Installation
------------

After this, you can install NWSAPy through ``pip``::

	pip install nwsapy

Once it's installed, go ahead and test it with this small script and replace the email field in ``set_user_agent()``:

.. code-block:: python

	import nwsapy
	
	nwsapy.set_user_agent("NWSAPy", "your_email@email.com")
	server_ping = nwsapy.ping_server()
	print(server_ping.status)
	

This should give you::

	OK


Note: The NWS API does require a ``User Agent``. NWSAPy gives funcitonality so that you're able to set this field (and other kinds of header information). This can be set with ``nwsapy.set_user_agent()``.

NWSAPy Architecture
-------------------



