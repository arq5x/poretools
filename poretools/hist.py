import sys
import time
import Fast5File
import rpy2.robjects as robjects
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects.packages import importr
from watchdog.observers import Observer
from collections import Counter

#logging
import logging
logger = logging.getLogger('poretools')
logger.setLevel(logging.INFO)

def plot_hist(sizes, args):
    """
    Use rpy2 to plot a histogram of the read sizes
    """
    r = robjects.r
    r.library("ggplot2")
    grdevices = importr('grDevices')

    sizes = robjects.IntVector([s for s in sizes \
                if s < args.max_length and s > args.min_length])

    sizes_min = min(sizes)
    sizes_max = max(sizes)

    binwidth = (sizes_max - sizes_min) / args.num_bins

    d = {'sizes' : sizes}
    df = robjects.DataFrame(d)

    # plot
    gp = ggplot2.ggplot(df)

    if not args.theme_bw:
        pp = gp + ggplot2.aes_string(x='sizes') \
                + ggplot2.geom_histogram(binwidth=binwidth)
    else:
        pp = gp + ggplot2.aes_string(x='sizes') \
            + ggplot2.geom_histogram(binwidth=binwidth) \
            + ggplot2.theme_bw()            

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
