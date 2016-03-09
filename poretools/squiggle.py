import os
import sys
import pandas as pd
import seaborn as sns
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from matplotlib import pyplot as plt

#logging
import logging
logger = logging.getLogger('poretools')

import Fast5File

def plot_squiggle(args, filename, start_times, mean_signals):
    """
    create a squiggle plot of the read
    """

    # set t_0 as the first measured time for the read.
    t_0 = start_times[0]
    total_time = start_times[-1] - start_times[0]
    # adjust times to be relative to t_0
    start_times = [t - t_0 for t in start_times]

    # infer the appropriate number of events given the number of facets
    num_events = len(mean_signals)
    events_per_facet = (num_events / args.num_facets) + 1
    # dummy variable to control faceting
    facet_category = [(i / events_per_facet) + 1 for i in range(len(start_times))]

    # make a data frame of the start times and mean signals
    d = {'start': start_times, 'mean': mean_signals, 'cat': facet_category}
    df = pd.DataFrame(d)

    starts = df.groupby('cat')['start']
    mins, maxs = list(starts.min()), list(starts.max())

    grid = sns.FacetGrid(df, row="cat", sharex=False, size=8)
    #plt.gcf().tight_layout()
    grid.fig.suptitle('Squiggle plot for read: ' + filename + "\nTotal time (sec): " + str(total_time))
    grid.map(plt.step, "start", "mean", marker=',', lw=1.0, where="mid")
    for i, ax in enumerate(grid.axes.flat):
        ax.set_xlim(mins[i], maxs[i])

    if args.saveas is not None:
        plot_file = os.path.basename(filename) + "." + args.saveas
        plt.savefig(plot_file)
    else:
        plt.show()

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
