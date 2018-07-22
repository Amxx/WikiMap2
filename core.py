#!/usr/bin/python3

import argparse
import itertools
import threading
import sys
import time
import wikimap
import zmq

class Server:
	def source_routine(wm, url='tcp://*:5555', context=None):
		context = context or zmq.Context()
		source = context.socket(zmq.REP)
		source.bind(url)
		try:
			sys.stdout.write('Source socket ready !\n')
			for i in range(args.limit) if args.limit else itertools.count():
				# Select random page
				idx = wikimap.accessor.get_waiting(wm)
				wp  = wm.data.get(idx)
				if not wp is None:
					# Wait for signal
					_ = source.recv()
					# Send job details
					source.send_pyobj({
						# 'idx': idx,
						'frg': wp.fragment,
						'url': wm.domain + wp.fragment
					})
				else:
					sys.stdout.write('No work to provide\n')
					time.sleep(1)
		except zmq.error.ContextTerminated:
			pass

	def sink_routine(wm, url='tcp://*:5556', context=None, verbose=False):
		context = context or zmq.Context()
		sink = context.socket(zmq.PULL)
		sink.bind('tcp://*:5556')
		try:
			sys.stdout.write('Sink socket ready !\n')
			offset = len(wm.data) - len(wm.pend) + 1
			for i in itertools.count(start=offset):
				# Receive and process report
				wp = wikimap.job.ingest(wm, sink.recv_pyobj())
				if verbose:
					sys.stdout.write('[{}] processed {}: {} links found\n'.format(i, wp.readable, len(wp.links)))
				# Every now and then, save the database
				if not args.discard and i % args.step == 0:
					wikimap.io.save(wm, file=args.db, verbose=True)
		except zmq.error.ContextTerminated:
			pass


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode',   type=str, choices=['load', 'init'], default='load')
	parser.add_argument(      '--db',     type=str,                           default='db.pkl')
	parser.add_argument(      '--step',   type=int,                           default=10000)
	parser.add_argument(      '--domain', type=str,                           default='https://fr.wikipedia.org/wiki/')
	parser.add_argument(      '--source', type=str,                           default='tcp://*:5555')
	parser.add_argument(      '--sink',   type=str,                           default='tcp://*:5556')
	parser.add_argument(      '--limit',  type=int,                           default=None)
	parser.add_argument(      '--discard', action='store_true')
	args = parser.parse_args()

	context = zmq.Context()

	if args.mode == 'load':
		wm = wikimap.io.load(file=args.db, verbose=True)
	else:
		wm = wikimap.WikiMap(domain=args.domain)

	sys.stdout.write('{:-^40}\n'.format(''))
	wikimap.io.show(wm)
	sys.stdout.write('{:-^40}\n'.format(''))

	try:
		thread = threading.Thread(target=Server.source_routine, args=(wm, args.source, context))
		thread.start()
		Server.sink_routine(wm, args.sink, context=context, verbose=True)

	except KeyboardInterrupt:
		sys.stdout.write('\n{:-^40}\n'.format(' Interrupted '))

	finally:
		context.term()
		wikimap.io.show(wm)
		if not args.discard:
			wikimap.io.save(wm, file=args.db, verbose=True)
