#!/usr/bin/python

import argparse
import itertools
import sys
import zmq

import wikimap

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode',     type=str, choices=['master', 'slave'], default='slave')
	parser.add_argument('-f', '--fragment', type=str,                              default=None)
	parser.add_argument('-d', '--domain',   type=str,                              default='https://fr.wikipedia.org/wiki/')
	parser.add_argument(      '--source',   type=str,                              default='tcp://localhost:5555')
	parser.add_argument(      '--sink',     type=str,                              default='tcp://localhost:5556')
	args = parser.parse_args()

	context = zmq.Context()

	source = context.socket(zmq.REQ)
	source.setsockopt(zmq.LINGER,   1000)
	source.setsockopt(zmq.RCVTIMEO, 10000)
	source.setsockopt(zmq.SNDTIMEO, 10000)
	source.connect(args.source)

	sink = context.socket(zmq.PUSH)
	sink.setsockopt(zmq.LINGER,   1000)
	sink.setsockopt(zmq.SNDTIMEO, 10000)
	sink.connect(args.sink)

	try:
		if args.mode == 'slave':
			for i in itertools.count():
				# Get job
				source.send(b'')
				job = source.recv_pyobj()
				# Verbose
				sys.stdout.write('[{}] New job: '.format(i))
				sys.stdout.flush()
				# Process
				job = wikimap.tools.job_process(job, verbose=True)
				# Send result
				sink.send_pyobj(job)

		elif args.mode == 'master' and args.fragment:
			# Define & process job
			# frg = args.fragment
			frg = wikimap.tools.quote(args.fragment)
			job = wikimap.tools.job_process({ 'frg': frg, 'url': args.domain+frg }, verbose=True)
			# Send result
			sink.send_pyobj(job)


	except KeyboardInterrupt:
		sys.stdout.write('\n{:-^40}\n'.format(' Interrupted '))

	except zmq.error.Again:
		sys.stdout.write('\n{:-^40}\n'.format(' Connection lost '))

	finally:
		source.close()
		sink.close()
		context.term()
