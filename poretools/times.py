## parse the output of this to make a collectors curve of reads
## this only works with >=1.10 metrichor output

#a=read.table("/tmp/times.txt", header=T, sep="\t")
#b=cbind(a, "start" = a$timestamp - min(a$timestamp))
#c=cut(b$start, seq(3600, 259200, by=3600)
#cumfreq0=c(0, cumsum(f))
#breaks = seq(3600, 259200, by=3600)
#plot(breaks/3600, cumfreq0)
#lines(breaks/3600, cumfreq0)
import Fast5File
from time import strftime, localtime
import sys

def run(parser, args):
	print '\t'.join(['filename', 'exp_starttime', 'unix_timestamp', 'iso_timestamp', 'day', 'hour', 'minute'])
	
	for fast5 in Fast5File.Fast5FileSet(args.files):
		if fast5.is_open:
			start_time = fast5.get_start_time()
			if start_time is None:
				print >>sys.stderr, "No start time for %s!" % (fast5.filename)
				fast5.close()
				continue

			lt = localtime(start_time)
			print "\t".join([fast5.filename, fast5.get_exp_start_time(),
				str(start_time), \
				strftime('%Y-%m-%dT%H:%M:%S%z', lt),
				strftime('%d', lt),
				strftime('%H', lt),
				strftime('%M', lt)])
			fast5.close()
