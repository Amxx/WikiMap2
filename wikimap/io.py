#!/usr/bin/python

import pickle
import sys

def save(wm, file, verbose=False):
	with open(file, 'wb') as output:
		if verbose:
			sys.stdout.write('saving database ... ')
			sys.stdout.flush()
		pickle.dump(wm, output, pickle.HIGHEST_PROTOCOL)
		if verbose:
			sys.stdout.write('done\n')

def load(file, verbose=False):
	with open(file, 'rb') as input:
		if verbose:
			sys.stdout.write('loading database ... ')
			sys.stdout.flush()
		wm = pickle.load(input)
		if verbose:
			sys.stdout.write('done\n')
		return wm

def show(wm):
	sys.stdout.write('{:>15,} processed pages\n{:>15,} pending pages\n{:>15,} total pages\n{:>15,} links\n'.format(
		len(wm.data) - len(wm.pend),
		len(wm.pend),
		len(wm.data),
		sum(len(wikipage.links) for wikipage in wm.data.values() if not wikipage.links is None)
	))
