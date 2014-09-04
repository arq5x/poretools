import Fast5File
from time import strftime, localtime
import sys

#logging
import logging
logger = logging.getLogger('poretools')

def run(parser, args):
	print '\t'.join(['channel', 'filename', 'read_length', 
		'exp_starttime', 'unix_timestamp', 'duration', 
		'unix_timestamp_end', 'iso_timestamp', 'day', 
		'hour', 'minute'])
	
	for fast5 in Fast5File.Fast5FileSet(args.files):
		if fast5.is_open:
			
			fq = fast5.get_fastq()
			
			start_time = fast5.get_start_time()
			if start_time is None:
				logger.warning("No start time for %s!" % (fast5.filename))
				fast5.close()
				continue

			if fq is not None:
				read_length = len(fq.seq)
			else:
				read_length = 0

			lt = localtime(start_time)
			print "\t".join([fast5.get_channel_number(),
				fast5.filename, 
				str(read_length),
				fast5.get_exp_start_time(),
				str(start_time), \
				str(fast5.get_duration()),
				str(fast5.get_end_time()),
				strftime('%Y-%m-%dT%H:%M:%S%z', lt),
				strftime('%d', lt),
				strftime('%H', lt),
				strftime('%M', lt)])
			fast5.close()
