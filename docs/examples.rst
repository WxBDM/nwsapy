Examples
========

.. _example1:

Example 1: Asynchronous Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's suppose you're putting togther an application that requires asynchronous programming. NWSAPy doesn't support this directly, but one workaround is utilizing ``await asyncio.sleep()``. The following example shows a method that allows for asynchronous programming:

.. code-block:: python

	import nwsapi
	import asyncio
	
	async def tor_warnings(self):	
		while connection_to_server.is_active():
			# get all of the active alerts
			active_alerts = nwsapi.get_active_alerts()
		
			# filter by tornado warning
			tor_warnings = active_alerts.filter_by("Tornado Warning")
		
			# get all of the polygons of the tornado warning
			self.tor_polygons = [warning.polygon for warning in tor_warnings]
			
			# get a list of when tornado warnings will expire
			all_expire = [warning.expires for warning in tor_warnings]
			
			# sort the when the first tornado warning will expire
			# note that this is a list comprised of `datetime` objects.
			self.expire_first = sorted(all_expire)
			
			# store which areas are affected
			self.affected_areas = [warning.areaDesc for warning in tor_warnings]
		
			await asyncio.sleep(45) # sleep for 45 seconds

	# create a task running in the background
	self.application.create_task(tor_warnings_every_45_seconds)