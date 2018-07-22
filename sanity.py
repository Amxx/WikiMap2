#!/usr/bin/python3

import argparse
import sys
import wikimap

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--db',  type=str, default='db.pkl')
	args = parser.parse_args()

	wm = wikimap.io.load(file=args.db, verbose=True)
	wikimap.io.show(wm)

	assert(len(wm.idxs) == len(wm.data))

	for idx, wp in wm.data.items():
		if not idx == wm.idxs[wp.fragment]:
			print('IDX ERROR\n{}\n{}\n{}'.format(idx, wm.idxs[wp.fragment], wp.fragment))
			exit(1)

		frg = wikimap.quote(wp.readable)
		if not frg == wp.fragment:
			print('QUOTE ERROR @ {}\n{}\n{}'.format(idx, wp.fragment, frg))
			exit(1)

	for frg, idx in wm.idxs.items():
		if not frg == wm.data.get(idx).fragment:
			print('FRAGMENT ERROR @ {}\n{}\n{}'.format(idx, frg, wm.data.get(idx).fragment))
			exit(1)

	for i in range(1, len(wm.idxs)+1):
		if i not in wm.data:
			print('DATA GAP ERROR @ {}'.format(i))
			exit(1)

	print('sanity check completed !')
