import os
import sys
import rpy2.robjects as robjects
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects.packages import importr

#logging
import logging
logger = logging.getLogger('poretools')

import Fast5File

def plot_squiggle(args, filename, start_times, mean_signals):
	"""
	Use rpy2 to create a squiggle plot of the read
	"""
	r = robjects.r
	r.library("ggplot2")
	grdevices = importr('grDevices')

	# set t_0 as the first measured time for the read.
	t_0 = start_times[0]
	total_time = start_times[-1] - start_times[0]
	# adjust times to be relative to t_0
	r_start_times = robjects.FloatVector([t - t_0 for t in start_times])
	r_mean_signals = robjects.FloatVector(mean_signals)
	
	# infer the appropriate number of events given the number of facets
	num_events = len(r_mean_signals)
	events_per_facet = (num_events / args.num_facets) + 1
	# dummy variable to control faceting
	facet_category = robjects.FloatVector([(i / events_per_facet) + 1 for i in range(len(start_times))])

	# make a data frame of the start times and mean signals
	d = {'start': r_start_times, 'mean': r_mean_signals, 'cat': facet_category}
	df = robjects.DataFrame(d)

	gp = ggplot2.ggplot(df)
	if not args.theme_bw:
		pp = gp + ggplot2.aes_string(x='start', y='mean') \
			+ ggplot2.geom_step(size=0.25) \
			+ ggplot2.facet_wrap(robjects.Formula('~cat'), ncol=1, scales="free_x") \
			+ ggplot2.scale_x_continuous('Time (seconds)') \
			+ ggplot2.scale_y_continuous('Mean signal (picoamps)') \
			+ ggplot2.ggtitle('Squiggle plot for read: ' + filename + "\nTotal time (sec): " + str(total_time)) \
			+ ggplot2.theme(**{'plot.title': ggplot2.element_text(size=11)})
	else:
		pp = gp + ggplot2.aes_string(x='start', y='mean') \
			+ ggplot2.geom_step(size=0.25) \
			+ ggplot2.facet_wrap(robjects.Formula('~cat'), ncol=1, scales="free_x") \
			+ ggplot2.scale_x_continuous('Time (seconds)') \
			+ ggplot2.scale_y_continuous('Mean signal (picoamps)') \
			+ ggplot2.ggtitle('Squiggle plot for read: ' + filename + "\nTotal time (sec): " + str(total_time)) \
			+ ggplot2.theme(**{'plot.title': ggplot2.element_text(size=11)}) \
			+ ggplot2.theme_bw()

	if args.saveas is not None:
		plot_file = os.path.basename(filename) + "." + args.saveas
		if os.path.isfile(plot_file):
			raise Exception('Cannot create plot for %s: plot file %s already exists' % (filename, plot_file))
		if args.saveas == "pdf":
			grdevices.pdf(plot_file, width = 8.5, height = 11)
		elif args.saveas == "png":
			grdevices.png(plot_file, width = 8.5, height = 11, 
				units = "in", res = 300)
		pp.plot()
		grdevices.dev_off()
	else:
		pp.plot()
		# keep the plot open until user hits enter
		print('Type enter to exit.')
		raw_input()

def do_plot_squiggle(args, fast5):
	start_times = []
	mean_signals = []

	for event in fast5.get_template_events():
		start_times.append(event.start)
		mean_signals.append(event.mean)

	if start_times:
		plot_squiggle(args, fast5.filename, start_times, mean_signals)
	else:
		logger.warning("Could not extract template events for read: %s.\n" \
			% fast5.filename)

	fast5.close()


def run(parser, args):

	fast5_set = Fast5File.Fast5FileSet(args.files)

	first_fast5 = fast5_set.next()
	for fast5 in fast5_set:
		# only create a squiggle plot for multiple reads if saving to file.
		if args.saveas is None:
			sys.exit("""Please use --saveas when plotting"""
					 """ multiple FAST5 files as input.\n""")
		if first_fast5 is not None:
			do_plot_squiggle(args, first_fast5)
			first_fast5 = None
		do_plot_squiggle(args, fast5)

	if first_fast5 is not None:
		do_plot_squiggle(args, first_fast5)
