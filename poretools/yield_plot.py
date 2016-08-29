import Fast5File
import matplotlib
matplotlib.use('Agg') # Must be called before any other matplotlib calls
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
import seaborn as sns

#logging
import logging
logger = logging.getLogger('poretools')
logger.setLevel(logging.INFO)

def plot_collectors_curve(args, start_times, read_lengths):
        """
        collectors curve of the run
        """
        # set t_0 as the first measured time for the read.
        t_0 = start_times[0]

        # adjust times to be relative to t_0
        start_times = [float(t - t_0) / float(3600) + 0.00000001 for t in start_times]

        # compute the cumulative based on reads or total base pairs
        if args.plot_type == 'reads':
                y_label = "Total reads"
                cumulative = np.cumsum(range(len(start_times)))
        elif args.plot_type == 'basepairs':
                y_label = "Total base pairs"
                cumulative = np.cumsum(read_lengths)

        step = args.skip
        # make a data frame of the lists
        d = {'start': [start_times[n] for n in xrange(0, len(start_times), step)],
             'lengths': [read_lengths[n] for n in xrange(0, len(read_lengths), step)],
             'cumul': [cumulative[n] for n in xrange(0, len(cumulative), step)]}
        df = pd.DataFrame(d)

        if args.savedf:
            df.to_csv(args.savedf, sep="\t")

        # title
        total_reads = len(read_lengths)
        total_bp = sum(read_lengths)
        plot_title = "Yield: " \
                + str(total_reads) + " reads and " \
                + str(total_bp) + " base pairs."

        if args.theme_bw:
            sns.set_style("whitegrid")

        # plot
        plt.plot(df['start'], df['cumul'])
        plt.xlabel('Time (hours)')
        plt.ylabel(y_label)
        plt.title(plot_title)

        if args.saveas is not None:
            plot_file = args.saveas
            plt.savefig(plot_file, figsize=(8.5, 8.5))
        else:
            plt.show()

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

