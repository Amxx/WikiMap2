#!/usr/bin/python3

import argparse
import collections
import itertools
import matplotlib.pyplot as plt
import numpy
import random
import sys
import wikimap

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
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

	x = numpy.arange(start=0, stop=len(wm.idxs)-len(wm.pend)+1)
	y = numpy.zeros_like(x)
	z = numpy.zeros_like(x)

	visited    = set()
	accessible = set()
	heap       = collections.deque()

	accessible.add(1)
	heap.append(1)

	while heap:
		idx = heap.popleft()
		wp  = wm.data.get(idx)
		visited.add(idx)
		for i in wp.links:
			if not i in accessible:
				accessible.add(i)
				if not wm.data.get(i).links is None:
					heap.append(i)
		y[len(visited)] = len(accessible)
		z[len(visited)] = len(wp.links)

	z = z.cumsum()

	plt.figure(figsize=(16,9))
	ax1 = plt.gca()
	ax2 = ax1.twinx()

	p1 = ax1.plot(x[1::100], x[1::100], color='#03A9F4')
	p2 = ax1.plot(x[1::100], y[1::100], color='#4CAF50')
	p3 = ax2.plot(x[1::100], z[1::100], color='#FBC02D')

	plt.legend((p1[0], p2[0], p3[0]), ('processed', 'accessible', 'links'), loc="upper left")
	ax1.set_xlabel('visited pages')
	ax1.set_ylabel('processed / accessible pages')
	ax2.set_ylabel('total links count')

	ax1.set_xlim(0,   300000)
	ax1.set_ylim(0,  3000000)
	ax2.set_ylim(0, 31000000)
	ax1.spines['top'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax1.xaxis.set_ticks_position('bottom')
	ax1.yaxis.set_ticks_position('left')
	ax2.yaxis.set_ticks_position('right')

	plt.show()
