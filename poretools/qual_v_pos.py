import Fast5File
from collections import defaultdict
import pandas
import sys
import matplotlib.pyplot as plt

#logging
import logging
logger = logging.getLogger('poreminion')
logger.setLevel(logging.INFO)

def run(parser, args):
    """ returns boxplot with qual scores for each bin/position"""
    qualpos = defaultdict(list)
    bin_width = args.bin_width
    
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

        fqs = fast5.get_fastqs(args.type)
        if args.high_quality:
                if fast5.get_complement_events_count() <= \
                   fast5.get_template_events_count():
                        fast5.close()
                        continue

        for fq in fqs:
                if fq is None or len(fq.seq) < args.min_length or len(fq.seq) > args.max_length:			
                        continue

                ctr = 0
                for q in fq.qual:
                    ctr += 1
                    qualpos[1+int(ctr//bin_width)].append(ord(q)-33)

        fast5.close()

    if args.saveas is not None:
        plt.switch_backend('Agg') # Use non-interactive backend in case this is
                                  # running on a headless system.

    logger.info("Processing data...")
    data = [qualpos[e] for e in sorted(qualpos.keys())]
    logger.info("Constructing box plot...")
    plt.boxplot(data)
    xdetail = " (" + str(bin_width) + " bp bins)"
    plt.xlabel("Bin number in read" + xdetail)
    plt.ylabel("Quality score")
    plt.xticks(rotation=65, fontsize=8)
    if args.saveas is not None:
            logger.info("Writing plot to file...")
            plot_file = args.saveas
            if plot_file.endswith(".pdf") or plot_file.endswith(".png") or plot_file.endswith(".svg"):
                    plt.savefig(plot_file)
            else:
                    logger.error("Unrecognized extension for %s! Try .pdf, .png, or .svg" % (plot_file))
                    sys.exit()

    else:
            logger.info("Showing plot...")
            plt.show()


