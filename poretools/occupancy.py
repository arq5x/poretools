import Fast5File
from time import strftime, localtime
from collections import defaultdict, Counter
import rpy2.robjects.lib.ggplot2 as gg
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import sys
import string
import random

#logging
import logging
logger = logging.getLogger('poretools')

def minion_flowcell_layout():
	seeds = [125,121,117,113,109,105,101,97,
	         93,89,85,81,77,73,69,65,
	         61,57,53,49,45,41,37,33,
	         29,25,21,17,13,9,5,1]
	
	flowcell_layout = []
	for s in seeds:
		for block in range(4):
			for row in range(4):
				flowcell_layout.append(s + 128*block + row)
	return flowcell_layout

def plot_read_count(parser, args, tot_reads_per_pore):
	"""
	Plot the pore performance
	"""
	r = robjects.r
	r.library("ggplot2")
	grdevices = importr('grDevices')

	flowcell_layout = minion_flowcell_layout()

	pore_values = []
	for pore in flowcell_layout:
		if pore in tot_reads_per_pore:
			pore_values.append(tot_reads_per_pore[pore])
		else:
			pore_values.append(0)		
	
	# make a data frame of the lists
	d = {'rownum': robjects.IntVector(range(1,17)*32),
		 'colnum': robjects.IntVector(sorted(range(1,33)*16)),
		 'tot_reads': robjects.IntVector(pore_values),
		 'labels': robjects.IntVector(flowcell_layout)
		 }

	df = robjects.DataFrame(d)
	gp = gg.ggplot(df)
	pp = gp + gg.aes_string(y = 'factor(rownum, rev(rownum))', \
		                         x = 'factor(colnum)') \
            + gg.geom_point(gg.aes_string(color='tot_reads'), size = 7) \
            + gg.geom_text(gg.aes_string(label ='labels'), colour="white", size = 2) \
            + gg.scale_colour_gradient2(low = "black", mid= "black", high="red") \
            + gg.coord_fixed(ratio=1.4) \
            + gg.labs(x=gg.NULL, y=gg.NULL)

	if args.saveas is not None:
		plot_file = args.saveas
		if plot_file.endswith(".pdf"):
			grdevices.pdf(plot_file, width = 11, height = 8.5)
		elif plot_file.endswith(".png"):
			grdevices.png(plot_file, width = 11, height = 8.5, 
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


def plot_total_bp(parser, args, tot_bp_per_pore):
	"""
	Plot the pore performance
	"""
	import math
	r = robjects.r
	r.library("ggplot2")
	grdevices = importr('grDevices')

	flowcell_layout = minion_flowcell_layout()

	pore_values = []
	for pore in flowcell_layout:
		if pore in tot_bp_per_pore:
			pore_values.append(math.log10(tot_bp_per_pore[pore]))
		else:
			pore_values.append(0)		
	
	# make a data frame of the lists
	d = {'rownum': robjects.IntVector(range(1,17)*32),
		 'colnum': robjects.IntVector(sorted(range(1,33)*16)),
		 'log10_tot_bp': robjects.IntVector(pore_values),
		 'labels': robjects.IntVector(flowcell_layout)
		 }

	df = robjects.DataFrame(d)
	gp = gg.ggplot(df)
	pp = gp + gg.aes_string(y = 'factor(rownum, rev(rownum))', \
		                         x = 'factor(colnum)') \
            + gg.geom_point(gg.aes_string(color='log10_tot_bp'), size = 7) \
            + gg.geom_text(gg.aes_string(label ='labels'), colour="white", size = 2) \
            + gg.scale_colour_gradient2(low = "black", mid= "black", high="red") \
            + gg.coord_fixed(ratio=1.4) \
            + gg.labs(x=gg.NULL, y=gg.NULL)

	if args.saveas is not None:
		plot_file = args.saveas
		if plot_file.endswith(".pdf"):
			grdevices.pdf(plot_file, width = 11, height = 8.5)
		elif plot_file.endswith(".png"):
			grdevices.png(plot_file, width = 11, height = 8.5, 
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

	tot_reads_per_pore = Counter()
	tot_bp_per_pore = Counter()

	print "\t".join(['channel_number', 'start_time', 'duration'])
	for fast5 in Fast5File.Fast5FileSet(args.files):
		if fast5.is_open:
			fq = fast5.get_fastq()
			
			start_time = fast5.get_start_time()
			if start_time is None:
				logger.warning("No start time for %s!" % (fast5.filename))
				fast5.close()
				continue

			pore_id = fast5.get_channel_number()
			tot_reads_per_pore[int(pore_id)] += 1
			tot_bp_per_pore[int(pore_id)] += len(fq.seq)

			lt = localtime(start_time)
			print "\t".join([
				str(pore_id),
				str(start_time),
				str(fast5.get_duration())])
			fast5.close()

	if args.plot_type == 'read_count':
		plot_read_count(parser, args, tot_reads_per_pore)
	elif args.plot_type == 'total_bp':
		plot_total_bp(parser, args, tot_bp_per_pore)


