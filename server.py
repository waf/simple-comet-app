#!/usr/bin/env python2.7
import cherrypy

# will be used to generate our fake messages
import itertools
import time
import random
import calendar
from datetime import datetime

class Comet(object):
	"""
	Comet-style asynchronous communication
	Based off of work done by Dan McDougall <YouKnowWho@YouKnowWhat.com>
	"""
	@cherrypy.expose
	def index(self, **kw):
		""" 
		Serve the client page via cherrypy to avoid cross-domain 
		restrictions
		"""
		f = open("client.html","r")
		return f.read()

	@cherrypy.expose
	def endpoint(self, **kw):
		"""Stream fake messages"""
		def msg_generator():
			timeout = 100
			random_range = 10
			elapsed_time = 0
			for n in itertools.count():
				if elapsed_time > timeout:
					return
				# pause for a random number of seconds
				pause = random.randint(0, random_range)
				time.sleep(pause)
				elapsed_time = elapsed_time + pause
				print("Yielding message %d" % n)
				yield self.build_fake_xml_message(n)
		return msg_generator()

	def build_fake_xml_message(self, message_number):
		xml_template = "<msg><index>%d</index><time>%d</time><name>%s</name></msg>"
		names = ["John","Sally","Bob","Mike","Will","Eve","Joe"]
		unix_time = calendar.timegm(datetime.now().utctimetuple())
		return xml_template % (message_number,unix_time,random.choice(names))

	# Enable streaming for the 'endpoint' method.
	endpoint._cp_config = {'response.stream': True}


if __name__ == "__main__":
	cherrypy.config.update({
		'log.screen':True,
		'tools.sessions.on': True,
		'checker.on':False
		})
	cherrypy.tree.mount(Comet(), config=None)
	cherrypy.engine.start()
	cherrypy.engine.block()
