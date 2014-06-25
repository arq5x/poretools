#!/usr/bin/env python

import sys
import numpy
import Fast5File

def run(parser, args):
	sizes = []
	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		fq = fast5.get_fastq()
		if fq is not None:
			sizes.append(len(fq.seq))
		fast5.close()

	print "total reads\t%f" % (len(sizes))
	print "total base pairs\t%f" % (sum(sizes))
	print "mean\t%f" % (numpy.mean(sizes))
	print "median\t%f" % (numpy.median(sizes))
	print "min\t%f" % (numpy.min(sizes))
	print "max\t%f" % (numpy.max(sizes))
