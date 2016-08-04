import sys
import time

import matplotlib
matplotlib.use('Agg') # Must be called before any other matplotlib calls
from matplotlib import pyplot as plt

import seaborn as sns
import Fast5File

import logging
logger = logging.getLogger('poretools')
logger.setLevel(logging.INFO)

def plot_hist(sizes, args):
    """
    plot a histogram of the read sizes
    """
    sizes = [s for s in sizes if args.min_length < s < args.max_length]

    if args.theme_bw:
        sns.set_style("whitegrid")
    plt.hist(sizes, args.num_bins)
    plt.xlabel('sizes')

    if args.saveas is not None:
        plt.savefig(args.saveas)
    else:
        plt.show()

def run(parser, args):
    sizes = []
    files_processed = 0

    for fast5 in Fast5File.Fast5FileSet(args.files):
        fq = fast5.get_fastq()
        if fq is not None:
            sizes.append(len(fq.seq))
        files_processed += 1
        if files_processed % 100 == 0:
            logger.info("%d files processed." % files_processed)
        fast5.close()
    plot_hist(sizes, args)

