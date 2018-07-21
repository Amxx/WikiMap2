#!/usr/bin/python3

import argparse
import sys

import wikimap

def print_wp_from_idx(wm, idx):
	wp = wm.data[idx]
	print(wp)
	print('{}: {} --- {}'.format(idx, wp.fragment, wp.readable))


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--db',  type=str, default='db.pkl')
	args = parser.parse_args()


	wm = wikimap.tools.db_load(file=args.db, verbose=True)

	wm.idxs['%C3%89mile_Bergeon'] = 1571247
	wm.data[1571247] = wikimap.WikiPage(fragment='%C3%89mile_Bergeon')

	# print(len(wm.idxs))
	# print(len(wm.data))

	# idx1 = wm.idxs.get('%C3%89mile_Bergeon')
	# idx2 = wm.idxs.get('Championnat_de_Malte_de_football_de_D1_1971-1972')

	# print(idx1)
	# print(idx2)

	# for idx, wp in wm.data.items():
	# 	if wp.fragment == '%C3%89mile_Bergeon':
	# 		print('found here: {}'.format(idx))
	# 	if wp.links and idx1 in wp.links:
	# 		print('pointed by: {}'.format(wp.readable))

	# for i in range(1585840):
	# 	if i not in wm.data:
	# 		print(i)


	# wikimap.tools.db_save(wm, file=args.db, verbose=True)

	print('done')