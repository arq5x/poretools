import sys
import Fast5File
import numpy as np
import pandas
import matplotlib.pyplot as plt

#logging
import logging
logger = logging.getLogger('poretools')
logger.setLevel(logging.INFO)

def plot_data_conc(sizes, args):
	"""
	Use matplotlib to plot a bar chart of total data (bp) vs. read sizes
	"""

	binwidth = args.bin_width
	reads = pandas.DataFrame(data=dict(lengths=sizes))
        high = max(reads['lengths'])
        if args.percent:
                scale = 100/float(sum(reads['lengths']))
        else:
                scale = 1
        # plot - taking a polygon approach
        # for each bin, get sum of read lengths that fall within that bin region
        # and plot bar/rectangle of that height over the bin region
        height = 0
        for i in range(0,high,binwidth):
                if args.cumulative:
                        height += scale*sum(reads['lengths'][reads['lengths'] > i][reads['lengths'] <= i+binwidth])
                else:
                        height = scale*sum(reads['lengths'][reads['lengths'] > i][reads['lengths'] <= i+binwidth])
                x = [i, i, i+binwidth,i+binwidth, i] # define x-dims of bar/rectangle (left, left, right, right, left)
                y = [0,height,height,0,0] # define y-dims of bar/rectangle (bottom, top, top, bottom, bottom).
                plt.fill(x, y, 'r') #plot bar/rectangle (color is red for now)
        if args.cumulative:
                plt.title("Cumulative Data Concentration Plot")
        else:
                plt.title("Data Concentration Plot")
        plt.xlabel("Read length (bp)")
        if args.percent:
                plt.ylabel("Percent of Data")	
        else:
                plt.ylabel("Data (bp)")	    	

        # saving or plotting to screen (user can save it from there as well)
	if args.saveas is not None:
		plot_file = args.saveas
		if plot_file.endswith(".pdf") or plot_file.endswith(".jpg"):
			plt.savefig(plot_file)
		else:
			logger.error("Unrecognized extension for %s! Try .pdf or .jpg" % (plot_file))
			sys.exit()

	else:
		plt.show()
	

def run(parser, args):
        if args.simulate:
                if args.parameters: ##fastest method is to just supply all paramaters
                        parameters = args.parameters.split(",")
                        readcount = int(parameters[0])
                        minsize = int(parameters[1])
                        maxsize = int(parameters[2])
                else:   ## find what was not provided out of: N, maxsize, defaultsize 
                        readcount = 0
                        files_processed = 0
                        minsize = float('inf')
                        maxsize = 0
                        for fast5 in Fast5File.Fast5FileSet(args.files):
                                if args.high_quality:
                                        if fast5.get_complement_events_count() <= \
                                           fast5.get_template_events_count():
                                                fast5.close()
                                                continue
                                if args.single_read:
                                        fqs = [fast5.get_fastq()]
                                else:
                                        fqs = fast5.get_fastqs(args.type)
                                for fq in fqs:
                                        if fq is not None:
                                                readcount += 1
                                                size = len(fq.seq)
                                                if size > maxsize:
                                                        maxsize = size
                                                elif size < minsize:
                                                        minsize = size
                                files_processed += 1
                                if files_processed % 100 == 0:
                                        logger.info("%d files processed." % files_processed)
                                fast5.close()
                                if args.min_length:
                                        minsize = int(args.min_length)
                                if args.max_length:
                                        maxsize = int(args.max_length)
                sizes = list(np.random.random_integers(minsize, maxsize, readcount))
                logger.info("parameters: N=%d, minsize=%d, maxsize=%d" % (readcount, minsize, maxsize))

        else:
                sizes = []
                files_processed = 0
                for fast5 in Fast5File.Fast5FileSet(args.files):
                        if args.start_time or args.end_time:
                                read_start_time = fast5.get_start_time()
                                read_end_time = fast5.get_end_time()
                                if args.start_time and args.start_time > read_start_time:
                                        fast5.close()
                                        continue
                                if args.end_time and args.end_time < read_end_time:
                                        fast5.close()
                                        continue
                        if args.high_quality:
                                if fast5.get_complement_events_count() <= \
                                   fast5.get_template_events_count():
                                        fast5.close()
                                        continue
                        if args.single_read:
                                fqs = [fast5.get_fastq()]
                        else:
                                fqs = fast5.get_fastqs(args.type)
                        for fq in fqs:
                                if fq is not None and not (len(fq.seq) < args.min_length or len(fq.seq) > args.max_length):
                                        sizes.append(len(fq.seq))
                                files_processed += 1
                        if files_processed % 100 == 0:
                                logger.info("%d files processed." % files_processed)
                        fast5.close()

	plot_data_conc(sizes, args)


