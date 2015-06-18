import sys
import time
from matplotlib import pyplot as plt
import seaborn as sns
import Fast5File
from watchdog.observers import Observer
from collections import Counter

import logging
logger = logging.getLogger('poretools')
logger.setLevel(logging.INFO)

def plot_hist(sizes, args):
    """
    plot a histogram of the read sizes
    """
    sizes = [s for s in sizes  if args.min_length < s < args.max_length]

    if args.theme_bw:
        sns.set_style("whitegrid")
    plt.hist(sizes, args.num_bins)

    if args.saveas is not None:
        plt.savefig(args.saveas)
    else:
        plt.show()

def run(parser, args):
    sizes = []
    files_processed = 0

    if args.watch is False:
        for fast5 in Fast5File.Fast5FileSet(args.files):
            fq = fast5.get_fastq()
            if fq is not None:
                sizes.append(len(fq.seq))
            files_processed += 1
            if files_processed % 100 == 0:
                logger.info("%d files processed." % files_processed)
            fast5.close()
        plot_hist(sizes, args)
    else:
        directory = args.files[0]
        observer = Observer()
        handler = Fast5File.Fast5DirHandler(directory)
        observer.schedule(handler, path=directory)
        observer.start()

        try:
            while True:
                time.sleep(5)
                for f in handler:
                    fast5 = Fast5File.Fast5File(f)
                    fq = fast5.get_fastq()
                    if fq is not None:
                        sizes.append(len(fq.seq))
                    files_processed += 1
                    if files_processed % 100 == 0:
                        logger.info("%d files processed." % files_processed)
                # TO DO
                # MAKE THIS CREATE AN UPDATED HISTOGRAM
                print Counter(sizes)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
