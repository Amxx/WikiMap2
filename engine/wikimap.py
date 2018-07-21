#!/usr/bin/python

import collections
import pickle
import random
import re
import urllib.parse
import urllib.request
import sys
import xml.dom.minidom

regexp = re.compile('^/wiki/([^:#]*)(#.*)?$')

class WikiPage:
	def __init__(self, fragment, links=None):
		self.fragment = fragment
		self.readable = urllib.parse.unquote(fragment)
		self.links    = links

class WikiMap:
	def __init__(self, domain='https://fr.wikipedia.org/wiki/'):
		self.idxs   = dict()
		self.data   = dict()
		self.pend   = set()
		self.domain = domain

class tools:
	def quote(url):
		return urllib.parse.quote(url, safe='!$()*,/;@~')

	def get_links(url):
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

	def job_process(job, verbose=False):
		if verbose:
			sys.stdout.write('processing `{}` ... '.format(urllib.parse.unquote(job['url'])))
			sys.stdout.flush()
		job['links'] = set(tools.get_links(job['url']))
		if verbose:
			sys.stdout.write('{} links found\n'.format(len(job['links'])))
		return job

	def job_ingest(wm, job):
		idx            = tools.get_index(wm, job['frg'])
		wikipage       = wm.data[idx]
		wikipage.links = { tools.get_index(wm, fragment) for fragment in job['links'] }
		wm.pend.discard(idx)
		return wikipage

	def dijkstra(wm, src, trg):
		route = dict()
		heap  = collections.deque()
		heap.append(src)
		while heap and not trg in route:
			idx = heap.popleft()
			wp  = wm.data.get(idx)
			for i in wp.links if wp.links else []:
				if not i in route:
					route[i] = idx
					heap.append(i)
		if trg in route:
			path = [ trg ]
			while not path[-1] is src:
				path.append(route[path[-1]])
			return [ wm.data.get(idx) for idx in path[::-1] ]
		else:
			return None

	def find_route(wm, frgsrc, frgtrg, network=True):
		src = tools.get_index(wm, frgsrc)
		trg = wm.idxs.get(frgtrg)
		if trg is None:
			sys.stderr.write('Target page is not in the database\n')
			return None
		if wm.data.get(src).links is None and network:
			wp = tools.job_ingest(wm,
				tools.job_process({
					'frg': frgsrc,
					'url': wm.domain+frgsrc
				}, verbose=False))
		return tools.dijkstra(wm, src, trg)

	def db_save(wm, file, verbose=False):
		with open(file, 'wb') as output:
			if verbose:
				sys.stdout.write('saving database ... ')
				sys.stdout.flush()
			pickle.dump(wm, output, pickle.HIGHEST_PROTOCOL)
			if verbose:
				sys.stdout.write('done\n')

	def db_load(file, verbose=False):
		with open(file, 'rb') as input:
			if verbose:
				sys.stdout.write('loading database ... ')
				sys.stdout.flush()
			wm = pickle.load(input)
			if verbose:
				sys.stdout.write('done\n')
			return wm

	def db_show(wm):
		sys.stdout.write('{:>15,} processed pages\n{:>15,} pending pages\n{:>15,} total pages\n{:>15,} links\n'.format(
			len(wm.data) - len(wm.pend),
			len(wm.pend),
			len(wm.data),
			sum(len(wikipage.links) for wikipage in wm.data.values() if not wikipage.links is None)
		))