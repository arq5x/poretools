import common
import Fast5File
from time import strftime, localtime

def run(parser, args):
	print '\t'.join(['filename', 'timestamp', 'time'])
	
	for filename in common.get_fast5_files(args.files):
		fast5 = Fast5File.Fast5File(filename)
		start_time = fast5.get_start_time()
		print "\t".join([filename, str(fast5.get_start_time()), strftime('%Y-%m-%dT%H:%M:%S%z', localtime(start_time))])
		fast5.close()
