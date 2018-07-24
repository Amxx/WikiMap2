#!/usr/bin/python

import random
import urllib.parse
import sys
import xml.dom.minidom

from ..WikiPage import WikiPage

def quote(url):
	return urllib.parse.quote(url, safe='!$()*,/;@~')

def get_index(wm, fragment):
	if not fragment in wm.idxs:
		idx = len(wm.idxs) + 1
		wm.idxs[fragment] = idx
		wm.data[idx     ] = WikiPage(fragment)
		wm.pend.add(idx)
	return wm.idxs.get(fragment)

def get_waiting(wm):
	try:
		# return next(iter(wm.pend))
		return random.sample(wm.pend, 1)[0]
	except ValueError:
		return None
