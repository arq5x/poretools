import os
import sys
import rpy2.robjects as robjects
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects.packages import importr


import common
import Fast5File

def plot_wiggle(filename, saveas, start_times, mean_signals):
	"""
	Use rpy2 to create a wiggle plot of the read
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
	# dummy variable to control faceting
	facet_category = robjects.FloatVector([i / 150 for i in range(len(start_times))])

	# make a data frame of the start times and mean signals
	d = {'start': r_start_times, 'mean': r_mean_signals, 'cat': facet_category}
	df = robjects.DataFrame(d)

	gp = ggplot2.ggplot(df)
	pp = gp + ggplot2.aes_string(x='start', y='mean') \
		+ ggplot2.geom_step() \
		+ ggplot2.facet_wrap(robjects.Formula('~cat'), ncol=1, scales="free_x") \
		+ ggplot2.scale_x_continuous('Total time ' + str(total_time) + ' seconds') \
		+ ggplot2.scale_y_continuous('Mean signal (picoamps)') \
		+ ggplot2.ggtitle('Wiggle plot for read: ' + filename) \
		+ ggplot2.theme(**{'plot.title': ggplot2.element_text(size=8)})

	if saveas is not None:
		plot_file = filename + "." + saveas
		if saveas == "pdf":
			grdevices.pdf(plot_file, width = 8.5, height = 11, 
				units = "in", res = 300)
		elif saveas == "png":
			grdevices.png(plot_file, width = 8.5, height = 11, 
				units = "in", res = 300)
		pp.plot()
		grdevices.dev_off()
	else:
		pp.plot()
		# keep the plot open until user hits enter
		print('Type enter to exit.')
		raw_input()

def run(parser, args):

	files = common.get_fast5_files(args.files)
	# only create a wiggle plot for multiple reads if saving to file.
	if len(files) > 1 and args.saveas is None:
		sys.stderr.write("Please use --saveas when plotting \
			              multiple FAST5 files as input.\n")
	
	for filename in files:
		fast5 = Fast5File.Fast5File(filename)

		start_times = []
		mean_signals = []
		
		for event in fast5.get_template_events():
			start_times.append(event.start)
			mean_signals.append(event.mean)		

		if start_times:
			plot_wiggle(filename, args.saveas, start_times, mean_signals)
		else:
			sys.stderr.write("Could not extract template events for read: %s.\n" \
				% filename)

		fast5.close()


