import Fast5File
from collections import Counter
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import logging
logger = logging.getLogger('poretools')

def minion_flowcell_layout():
    seeds = [125, 121, 117, 113, 109, 105, 101, 97,
             93, 89, 85, 81, 77, 73, 69, 65,
             61, 57, 53, 49, 45, 41, 37, 33,
             29, 25, 21, 17, 13, 9, 5, 1]

    flowcell_layout = []
    for s in seeds:
        for block in range(4):
            for row in range(4):
                    flowcell_layout.append(s + 128*block + row)
    return flowcell_layout

def plot_performance(parser, args, pore_measure):
    """
    Plot the pore performance in terms of reads per pore
    """
    flowcell_layout = minion_flowcell_layout()

    pore_values = []
    for pore in flowcell_layout:
        if pore in pore_measure:
            pore_values.append(pore_measure[pore])
        else:
            pore_values.append(0)

    # make a data frame of the lists
    d = {'rownum': range(1,17)*32,
        'colnum': sorted(range(1,33)*16),
        'tot_reads': pore_values,
        'labels': flowcell_layout}
    df = pd.DataFrame(d)

    d = df.pivot("rownum", "colnum", "tot_reads")
    sns.heatmap(d, annot=True, fmt="d", linewidths=.5)

    if args.saveas is not None:
        plot_file = args.saveas
        plt.savefig(plot_file, figsize=(8.5, 8.5))
    else:
        plt.show()

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

            print "\t".join([
                str(pore_id),
                str(start_time),
                str(fast5.get_duration())])
            fast5.close()

    if args.plot_type == 'read_count':
        plot_performance(parser, args, tot_reads_per_pore)
    elif args.plot_type == 'total_bp':
        plot_performance(parser, args, tot_bp_per_pore)


