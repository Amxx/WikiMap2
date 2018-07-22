#!/usr/bin/python

import urllib.parse

class WikiPage:
	def __init__(self, fragment, links=None):
		self.fragment = fragment
		self.readable = urllib.parse.unquote(fragment)
		self.links    = links
