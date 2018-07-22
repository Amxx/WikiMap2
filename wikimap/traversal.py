#!/usr/bin/python

import collections

from .accessor import get_index
from .job      import process, ingest

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
	src = get_index(wm, frgsrc)
	trg = wm.idxs.get(frgtrg)
	if trg is None:
		sys.stderr.write('Target page is not in the database\n')
		return None
	if wm.data.get(src).links is None and network:
		wp = ingest(wm, process({
				'frg': frgsrc,
				'url': wm.domain+frgsrc
			}, verbose=False))
	return dijkstra(wm, src, trg)
