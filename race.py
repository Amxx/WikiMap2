#!/usr/bin/python3

import argparse
import itertools
import sys
import wikimap

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('query', type=str, nargs=2)
	parser.add_argument('--db',  type=str, default='db.pkl')
	args = parser.parse_args()

	sys.stdout.write('loading database ... ')
	sys.stdout.flush()
	wm = wikimap.io.load(file=args.db)
	sys.stdout.write('done\n')
	sys.stdout.write('{:-^40}\n'.format(''))

	sys.stdout.write('Details:\n')
	wikimap.io.show(wm)
	sys.stdout.write('{:-^40}\n'.format(''))

	sys.stdout.write('Looking for route: {} → {}\n'.format(*args.query))
	sys.stdout.write('{:-^40}\n'.format(''))

	frgsrc = wikimap.quote(args.query[0])
	frgtrg = wikimap.quote(args.query[1])

	path = wikimap.traversal.find_route(wm, frgsrc, frgtrg)
	if path:
		for i, wp in zip(itertools.count(), path):
			sys.stdout.write('{: 5d} {}\n'.format(i, wp.readable))
	else:
		sys.stdout.write('No route found :(\n')
