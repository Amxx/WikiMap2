#!/usr/bin/python

import re
import urllib.parse
import urllib.request
import sys
import xml.dom.minidom

from ..accessor import get_index

regexp = re.compile('^/wiki/([^:#]*)(#.*)?$')

def links(url):
	try:
		raw = xml.dom.minidom.parseString(urllib.request.urlopen(url).read())
		cnt = next(el for el in raw.getElementsByTagName('div') if el.getAttribute('id') == 'content')
		for link in cnt.getElementsByTagName('a'):
			match = regexp.match(link.getAttribute('href'))
			if match and not match.group(1).startswith('Liste_'):
				yield match.group(1)
	except Exception as e:
		sys.stderr.write('ERROR: Exception parsing page: {}\n'.format(e))
	finally:
		yield from []

def process(job, verbose=False):
	if verbose:
		sys.stdout.write('processing `{}` ... '.format(urllib.parse.unquote(job['url'])))
		sys.stdout.flush()
	job['links'] = set(links(job['url']))
	if verbose:
		sys.stdout.write('{} links found\n'.format(len(job['links'])))
	return job

def ingest(wm, job):
	idx            = get_index(wm, job['frg'])
	wikipage       = wm.data[idx]
	wikipage.links = { get_index(wm, fragment) for fragment in job['links'] }
	wm.pend.discard(idx)
	return wikipage
