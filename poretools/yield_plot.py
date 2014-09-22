import Fast5File
from time import strftime, localtime
import rpy2.robjects.lib.ggplot2 as ggplot2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

#logging
import logging
logger = logging.getLogger('poretools')
logger.setLevel(logging.INFO)

def plot_collectors_curve(args, start_times, read_lengths):
	"""
	Use rpy2 to create a collectors curve of the run
	"""
	r = robjects.r
	r.library("ggplot2")
	grdevices = importr('grDevices')

	# set t_0 as the first measured time for the read.
	t_0 = start_times[0]

	# adjust times to be relative to t_0
	r_start_times = robjects.FloatVector([float(t - t_0) / float(3600) + 0.00000001 \
		for t in start_times])
	r_read_lengths = robjects.IntVector(read_lengths)

	# compute the cumulative based on reads or total base pairs
	if args.plot_type == 'reads':
		y_label = "Total reads"
		cumulative = \
			r.cumsum(robjects.IntVector([1] * len(start_times)))
	elif args.plot_type == 'basepairs':
		y_label = "Total base pairs"
		cumulative = r.cumsum(r_read_lengths)

	step = args.skip
	# make a data frame of the lists
	d = {'start': robjects.FloatVector([r_start_times[n] for n in xrange(0, len(r_start_times), step)]), 
		'lengths': robjects.IntVector([r_read_lengths[n] for n in xrange(0, len(r_read_lengths), step)]),
		'cumul': robjects.IntVector([cumulative[n] for n in xrange(0, len(cumulative), step)])}
	df = robjects.DataFrame(d)


	if args.savedf:
		robjects.r("write.table")(df, file=args.savedf, sep="\t")

	# title
	total_reads = len(read_lengths)
	total_bp = sum(read_lengths)
	plot_title = "Yield: " \
		+ str(total_reads) + " reads and " \
		+ str(total_bp) + " base pairs."

	# plot
	gp = ggplot2.ggplot(df)
	pp = gp + ggplot2.aes_string(x='start', y='cumul') \
		+ ggplot2.geom_step(size=2) \
		+ ggplot2.scale_x_continuous('Time (hours)') \
		+ ggplot2.scale_y_continuous(y_label) \
		+ ggplot2.ggtitle(plot_title)

        # extrapolation
	if args.extrapolate:
		start = robjects.ListVector({'a': 1, 'b': 1})
                pp = pp + ggplot2.stat_smooth(fullrange='TRUE', method='nls',
                                              formula='y~a*I((x*3600)^b)',
                                              se='FALSE', start=start) \
                        + ggplot2.xlim(0, float(args.extrapolate))

	if args.theme_bw:
		pp = pp + ggplot2.theme_bw()	

	if args.saveas is not None:
		plot_file = args.saveas
		if plot_file.endswith(".pdf"):
			grdevices.pdf(plot_file, width = 8.5, height = 8.5)
		elif plot_file.endswith(".png"):
			grdevices.png(plot_file, width = 8.5, height = 8.5, 
				units = "in", res = 300)
		else:
			logger.error("Unrecognized extension for %s!" % (plot_file))
			sys.exit()

		pp.plot()
		grdevices.dev_off()
	else:
		pp.plot()
		# keep the plot open until user hits enter
		print('Type enter to exit.')
		raw_input()

def run(parser, args):
	
	start_times = []
	read_lengths = []
	files_processed = 0
	for fast5 in Fast5File.Fast5FileSet(args.files):
		if fast5.is_open:
			
			fq = fast5.get_fastq()
			
			start_time = fast5.get_start_time()
			if start_time is None:
				logger.warning("No start time for %s!" % (fast5.filename))
				fast5.close()
				continue

			start_times.append(start_time)
			if fq is not None:
				read_lengths.append(len(fq.seq))
			else:
				read_lengths.append(0)
			fast5.close()

		files_processed += 1
		if files_processed % 100 == 0:
			logger.info("%d files processed." % files_processed)
	


	# sort the data by start time
	start_times, read_lengths = (list(t) for t in zip(*sorted(zip(start_times, read_lengths))))
	plot_collectors_curve(args, start_times, read_lengths)

