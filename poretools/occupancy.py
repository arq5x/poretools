import Fast5File
from time import strftime, localtime
import sys

#logging
import logging
logger = logging.getLogger('poretools')

def run(parser, args):
	print "\t".join(['channel_number', 'exp_start_time', 'start_time', 'duration'])
	for fast5 in Fast5File.Fast5FileSet(args.files):
		if fast5.is_open:
			fq = fast5.get_fastq()
			
			start_time = fast5.get_start_time()
			if start_time is None:
				logger.warning("No start time for %s!" % (fast5.filename))
				fast5.close()
				continue

			lt = localtime(start_time)
			print "\t".join([
				str(fast5.get_channel_number()),
				str(start_time),
				str(fast5.get_duration())])
			fast5.close()
