#!/usr/bin/env python

import os.path
import sys
import argparse

#logger
import logging
logger = logging.getLogger('poretools')

# poretools imports
from . import version

def run_subtool(parser, args):
    if args.command == 'combine':
        from . import combine as submodule
    elif args.command == 'events':
        from . import events as submodule
    elif args.command == 'fasta':
        from . import fasta as submodule
    elif args.command == 'fastq':
        from . import fastq as submodule
    elif args.command == 'hist':
        from . import hist as submodule
    elif args.command == 'metadata':
        from . import metadata as submodule
    elif args.command == 'nucdist':
        from . import nucdist as submodule
    elif args.command == 'occupancy':
        from . import occupancy as submodule
    elif args.command == 'qualdist':
        from . import qualdist as submodule
    elif args.command == 'qualpos':
        from . import qual_v_pos as submodule
    elif args.command == 'readstats':
        from . import readstats as submodule
    elif args.command == 'stats':
        from . import stats as submodule
    elif args.command == 'tabular':
        from . import tabular as submodule
    elif args.command == 'times':
        from . import times as submodule
    elif args.command == 'squiggle':
        from . import squiggle as submodule
    elif args.command == 'winner':
        from . import winner as submodule
    elif args.command == 'yield_plot':
        from . import yield_plot as submodule
    elif args.command == 'index':
        from . import index as submodule
    elif args.command == 'organise':
        from . import organise as submodule
    else:
        parser.print_help()
        exit()

    # run the chosen submodule.
    submodule.run(parser, args)

class ArgumentParserWithDefaults(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParserWithDefaults, self).__init__(*args, **kwargs)
        self.add_argument("-q", "--quiet", help="Do not output warnings to stderr",
                          action="store_true",
                          dest="quiet")
        self.set_defaults(func=run_subtool)

def main():
    logging.basicConfig()

    #########################################
    # create the top-level parser
    #########################################
    parser = ArgumentParserWithDefaults(prog='poretools', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", help="Installed poretools version",
                        action="version",
                        version="%(prog)s " + str(version.__version__))
    subparsers = parser.add_subparsers(title='[sub-commands]', dest='command', parser_class=ArgumentParserWithDefaults)

    #########################################
    # create the individual tool parsers
    #########################################

    ##########
    # combine
    ##########
    parser_combine = subparsers.add_parser('combine',
                                        help='Combine a set of FAST5 files in a TAR achive')
    parser_combine.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_combine.add_argument('-o',
                              dest='tar_filename',
                              metavar='STRING',
                              required=True,
                              help='The name of the output TAR archive for the set of FAST5 files.')
    parser_combine.set_defaults(func=run_subtool)


    ##########
    # FASTQ
    ##########
    parser_fastq = subparsers.add_parser('fastq',
                                        help='Extract FASTQ sequences from a set of FAST5 files')
    parser_fastq.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_fastq.add_argument('--type',
                              dest='type',
                              metavar='STRING',
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev', 'best'],
                              default='all',
                              help='Which type of FASTQ entries should be reported? Def.=all')
    parser_fastq.add_argument('--start',
                              dest='start_time',
                              default=None,
                              type=int,
                              help='Only report reads from after start timestamp')
    parser_fastq.add_argument('--end',
                              dest='end_time',
                              default=None,
                              type=int,
                              help='Only report reads from before end timestamp')
    parser_fastq.add_argument('--min-length',
                              dest='min_length',
                              default=0,
                              type=int,
                              help=('Minimum read length for FASTQ entry to be reported.'))
    parser_fastq.add_argument('--max-length',
                              dest='max_length',
                              default=-1,
                              type=int,
                              help=('Maximum read length for FASTQ entry to be reported.'))                          
    parser_fastq.add_argument('--high-quality',
                              dest='high_quality',
                              default=False,
                              action='store_true',
                              help=('Only report reads with more complement events than template.'))   
    parser_fastq.add_argument('--normal-quality',
                              dest='normal_quality',
                              default=False,
                              action='store_true',
                              help=('Only report reads with fewer complement events than template.'))
    parser_fastq.add_argument('--group',
                              dest='group',
                              default=0,
                              type=int,
                              help=('Base calling group serial number to extract, default 000'))
    parser_fastq.set_defaults(func=run_subtool)


    ##########
    # FASTA
    ##########
    parser_fasta = subparsers.add_parser('fasta',
                                        help='Extract FASTA sequences from a set of FAST5 files')
    parser_fasta.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_fasta.add_argument('--type',
                              dest='type',
                              metavar='STRING',
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev', 'best'],
                              default='all',
                              help='Which type of FASTQ entries should be reported? Def.=all')
    parser_fasta.add_argument('--start',
                              dest='start_time',
                              default=None,
                              type=int,
                              help='Only report reads from after start timestamp')
    parser_fasta.add_argument('--end',
                              dest='end_time',
                              default=None,
                              type=int,
                              help='Only report reads from before end timestamp')
    parser_fasta.add_argument('--min-length',
                              dest='min_length',
                              default=0,
                              type=int,
                              help=('Minimum read length for FASTA entry to be reported.'))
    parser_fasta.add_argument('--max-length',
                              dest='max_length',
                              default=-1,
                              type=int,
                              help=('Maximum read length for FASTA entry to be reported.'))                          
    parser_fasta.add_argument('--high-quality',
                              dest='high_quality',
                              default=False,
                              action='store_true',
                              help=('Only report reads with more complement events than template.'))
    parser_fasta.add_argument('--normal-quality',
                              dest='normal_quality',
                              default=False,
                              action='store_true',
                              help=('Only report reads with fewer complement events than template.'))
    parser_fasta.add_argument('--group',
                              dest='group',
                              default=0,
                              type=int,
                              help=('Base calling group serial number to extract, default 000'))
    parser_fasta.set_defaults(func=run_subtool)


    ##########
    # stats
    ##########
    parser_stats = subparsers.add_parser('stats',
                                        help='Get read size stats for a set of FAST5 files')
    parser_stats.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_stats.add_argument('--type',
                              dest='type',
                              metavar='STRING',
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev', 'best'],
                              default='all',
                              help='Which type of FASTQ entries should be reported? Def.=all')
    parser_stats.add_argument('--full-tsv',
                              dest='full_tsv',
                              default=False,
                              action='store_true',
                              help=('Verbose output in tab-separated format.'))
    parser_stats.add_argument('--group',
                              dest='group',
                              default=0,
                              type=int,
                              help=('Base calling group serial number to extract, default 000'))
    parser_stats.set_defaults(func=run_subtool)


    ##########
    # hist
    ##########
    parser_hist = subparsers.add_parser('hist',
                                        help='Plot read size histogram for a set of FAST5 files')
    parser_hist.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_hist.add_argument('--min-length',
                              dest='min_length',
                              default=0,
                              type=int,
                              help=('Minimum read length to be included in histogram.'))
    parser_hist.add_argument('--max-length',
                              dest='max_length',
                              default=1000000000,
                              type=int,
                              help=('Maximum read length to be included in histogram.'))
    parser_hist.add_argument('--num-bins',
                              dest='num_bins',
                              default=50,
                              type=int,
                              help=('The number of histogram bins.'))
    parser_hist.add_argument('--saveas',
                             dest='saveas',
                             metavar='STRING',
                             help='Save the plot to a file.',
                             default=None)
    parser_hist.add_argument('--theme-bw',
                             dest='theme_bw',
                             default=False,
                             action='store_true',
                             help="Use a black and white theme.")
    parser_hist.add_argument('--watch',
                             dest='watch',
                             default=False,
                             action='store_true',
                             help="Monitor a directory.")
    parser_hist.set_defaults(func=run_subtool)


    ###########
    # events
    ###########
    parser_events = subparsers.add_parser('events',
                                        help='Extract each nanopore event for each read.')
    parser_events.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_events.add_argument('--pre-basecalled',
                              dest='pre_basecalled',
                              default=False,
                              action='store_true',
                              help=('Report pre-basecalled events'))     
    parser_events.set_defaults(func=run_subtool)


    ###########
    # readstats
    ###########
    parser_readstats = subparsers.add_parser('readstats',
                                        help='Extract signal information for each read over time.')
    parser_readstats.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_readstats.set_defaults(func=run_subtool)


    ##########
    # tabular
    ##########
    parser_tabular = subparsers.add_parser('tabular',
                                        help='Extract the lengths and name/seq/quals from a set of FAST5 files in TAB delimited format')
    parser_tabular.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_tabular.add_argument('--type',
                              dest='type',
                              metavar='STRING',
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev', 'best'],
                              default='all',
                              help='Which type of FASTA entries should be reported? Def.=all')
    parser_tabular.set_defaults(func=run_subtool)

    #########
    # nucdist
    #########
    parser_nucdist = subparsers.add_parser('nucdist',
                                        help='Get the nucl. composition of a set of FAST5 files')
    parser_nucdist.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_nucdist.set_defaults(func=run_subtool)

    #########
    # metadata
    #########
    parser_metadata = subparsers.add_parser('metadata',
                                        help='Return run metadata such as ASIC ID and temperature from a set of FAST5 files')
    parser_metadata.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_metadata.add_argument('--read',
                              dest='read',
                              default=False,
                              action='store_true',
                              help=('Report read level metadata'))      
    parser_metadata.set_defaults(func=run_subtool)
    
    #########
    # index
    #########
    parser_index = subparsers.add_parser('index',
                                        help='Tabulate all file location info and metadata such as ASIC ID and temperature from a set of FAST5 files')
    parser_index.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_index.set_defaults(func=run_subtool)

    
    ##########
    # qualdist
    ##########
    parser_qualdist = subparsers.add_parser('qualdist',
                                        help='Get the qual score composition of a set of FAST5 files')
    parser_qualdist.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_qualdist.set_defaults(func=run_subtool)



    ##########
    # qual vs. position
    ##########
    parser_qualpos = subparsers.add_parser('qualpos',
                                        help='Get the qual score distribution over positions in reads')
    parser_qualpos.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_qualpos.set_defaults(func=run_subtool)
    parser_qualpos.add_argument('--min-length',
                              dest='min_length',
                              default=0,
                              type=int,
                              help=('Minimum read length to be included in analysis.'))
    parser_qualpos.add_argument('--max-length',
                              dest='max_length',
                              default=1000000000,
                              type=int,
                              help=('Maximum read length to be included in analysis.'))
    parser_qualpos.add_argument('--bin-width',
                              dest='bin_width',
                              default=1000,
                              type=int,
                              help=('The width of bins (default: 1000 bp).'))
    parser_qualpos.add_argument('--type',
                              dest='type',
                              metavar='STRING',
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev', 'best'],
                              default='all',
                              help='Which type of reads should be analyzed? Def.=all, choices=[all, fwd, rev, 2D, fwd,rev, best]')
    parser_qualpos.add_argument('--start',
                              dest='start_time',
                              default=None,
                              type=int,
                              help='Only analyze reads from after start timestamp')
    parser_qualpos.add_argument('--end',
                              dest='end_time',
                              default=None,
                              type=int,
                              help='Only analyze reads from before end timestamp')
    parser_qualpos.add_argument('--high-quality',
                              dest='high_quality',
                              default=False,
                              action='store_true',
                              help='Only analyze reads with more complement events than template.')

    parser_qualpos.add_argument('--saveas',
                             dest='saveas',
                             metavar='STRING',
                             help='''Save the plot to a file named filename.extension (e.g. pdf, jpg)''',
                             default=None)




    ##########
    # winner
    ##########
    parser_winner = subparsers.add_parser('winner',
                                        help='Get the longest read from a set of FAST5 files')
    parser_winner.add_argument('files', metavar='FILES', nargs='+',
                               help='The input FAST5 files.')
    parser_winner.add_argument('--type',
                              dest='type',
                              metavar='STRING',
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev', 'best'],
                              default='all',
                              help='Which type of FASTA entries should be reported? Def.=all')
    parser_winner.set_defaults(func=run_subtool)

    ###########
    # squiggle
    ###########
    parser_squiggle = subparsers.add_parser('squiggle',
                                        help='Plot the observed signals for FAST5 reads.')
    parser_squiggle.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_squiggle.add_argument('--saveas',
                             dest='saveas',
                             metavar='STRING',
                             choices=['pdf', 'png'],
                             help='Save the squiggle plot to a file.',
                             default=None)
    parser_squiggle.add_argument('--num-facets',
                              dest='num_facets',
                              metavar='INTEGER',
                              default=6,
                              type=int,
                              help=('The number of plot facets (sub-plots). More is better for long reads. (def=6)'))
    parser_squiggle.add_argument('--theme-bw',
                             dest='theme_bw',
                             default=False,
                             action='store_true',
                             help="Use a black and white theme.")

    parser_squiggle.set_defaults(func=run_subtool)

    ##########
    # times
    ##########
    parser_times = subparsers.add_parser('times',
                                        help='Return the start times from a set of FAST5 files in tabular format')
    parser_times.add_argument('files', metavar='FILES', nargs='+',
                               help='The input FAST5 files.')
    parser_times.set_defaults(func=run_subtool)

    ############
    # yield_plot
    ############
    parser_yield_plot = subparsers.add_parser('yield_plot',
                                        help='Plot the yield over time for a set of FAST5 files')
    parser_yield_plot.add_argument('files', metavar='FILES', nargs='+',
                               help='The input FAST5 files.')
    parser_yield_plot.add_argument('--saveas',
                             dest='saveas',
                             metavar='STRING',
                             help='Save the plot to a file. Extension (.pdf or .png) drives type.',
                             default=None)
    parser_yield_plot.add_argument('--plot-type',
                             dest='plot_type',
                             metavar='STRING',
                             choices=['reads', 'basepairs'],
                             help='Save the wiggle plot to a file (def=reads).',
                             default='reads')
    parser_yield_plot.add_argument('--theme-bw',
                             dest='theme_bw',
                             default=False,
                             action='store_true',
                             help="Use a black and white theme.")
    parser_yield_plot.add_argument('--skip',
                             dest='skip',
                             metavar='INTEGER',
                             type=int,
                             default=1,
                             help="Only plot every n points to reduce size")
    parser_yield_plot.add_argument('--savedf',
                             dest='savedf',
                             metavar='STRING',
                             help='Save the data frame used to construct plot to a file.',
                             default=None)

    parser_yield_plot.set_defaults(func=run_subtool)

    ############
    # yield_plot
    ############
    parser_occupancy = subparsers.add_parser('occupancy',
                                        help='Inspect pore activity over time for a set of FAST5 files')
    parser_occupancy.add_argument('files', metavar='FILES', nargs='+',
                               help='The input FAST5 files.')
    parser_occupancy.add_argument('--saveas',
                             dest='saveas',
                             metavar='STRING',
                             help='Save the plot to a file. Extension (.pdf or .png) drives type.',
                             default=None)
    parser_occupancy.add_argument('--plot-type',
                             dest='plot_type',
                             metavar='STRING',
                             choices=['read_count', 'total_bp'],
                             help='The type of plot to generate',
                             default='read_count')

    parser_occupancy.set_defaults(func=run_subtool)
    
    ##########
    # organise
    ##########

    parser_organise = subparsers.add_parser('organise',
                               help='Move FAST5 files into a useful folder hierarchy')
    parser_organise.add_argument('files', metavar='FILES', nargs='+',
                               help='The input FAST5 files.')
    parser_organise.add_argument('dest',
                               metavar='STRING',
                               help='The destination directory.')
    parser_organise.add_argument('--copy',
                               default=False,
                               action='store_true',
                               dest='copy', 
                               help='Make a copy of files instead of moving')

    parser_organise.set_defaults(func=run_subtool)

    #######################################################
    # parse the args and call the selected function
    #######################################################
    args = parser.parse_args()

    if args.quiet:
        logger.setLevel(logging.ERROR)

    try:
      args.func(parser, args)
    except IOError as e:
         if e.errno != 32:  # ignore SIGPIPE
             raise

if __name__ == "__main__":
    main()
