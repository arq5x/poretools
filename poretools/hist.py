import sys
import Fast5File
import rpy2.robjects as robjects

def plot_hist(sizes, args):
	"""
	Use rpy2 to plot a histogram of the read sizes
	"""
	r = robjects.r
	r_sizes = robjects.IntVector([s for s in sizes \
		if s < args.max_length and s > args.min_length])
	
	r.hist(r_sizes, breaks=args.num_bins,
		xlab='Read lengths', ylab='Count',
		main='Histogram of read lengths')

	# keep the plot open until user hits enter
	print('Type enter to exit.')
	raw_input()


def run(parser, args):
	sizes = []
	files_processed = 0
	for fast5 in Fast5File.Fast5FileSet(args.files):
		fq = fast5.get_fastq()
		if fq is not None:
			sizes.append(len(fq.seq))
		files_processed += 1
		if files_processed % 100 == 0:
			sys.stderr.write("LOG: %d files processed.\n" % files_processed)
		fast5.close()

	plot_hist(sizes, args)


