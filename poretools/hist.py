import matplotlib.pyplot as plt
import common
import Fast5File
import rpy2.robjects as robjects

def run(parser, args):
	sizes = []
	for filename in common.get_fast5_files(args.files):
		fast5 = Fast5File.Fast5File(filename)
		fq = fast5.get_fastq()
		if fq is not None:
			sizes.append(len(fq.seq))
		fast5.close()

	r = robjects.r
	r_sizes = robjects.IntVector([s for s in sizes \
		if s < args.max_length and s > args.min_length])
	
	r.hist(r_sizes, breaks=args.num_bins,
		xlab='Read lengths', ylab='Count',
		main='Histogram of read lengths')

	# keep the plot open until user hits enter
	print('Type enter to exit.')
	raw_input()


