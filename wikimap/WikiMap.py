#!/usr/bin/python

class WikiMap:
	def __init__(self, domain='https://fr.wikipedia.org/wiki/'):
		self.idxs   = dict()
		self.data   = dict()
		self.pend   = set()
		self.domain = domain
