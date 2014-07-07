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

def run(parser, args):
	print '\t'.join(['filename', 'timestamp', 'time'])
	
	for fast5 in Fast5File.Fast5FileSet(args.files):
		start_time = fast5.get_start_time()
		print "\t".join([fast5.filename, str(fast5.get_start_time()), \
			strftime('%Y-%m-%dT%H:%M:%S%z', localtime(start_time))])
		fast5.close()
