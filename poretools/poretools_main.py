#!/usr/bin/env python

import os.path
import sys
import argparse

# poretools imports
import stats
import hist
import fasta
import fastq
import nucdist
import qualdist
import readstats
import events
import tabular
import winner
import wiggle
import poretools.version


def main():

    #########################################
    # create the top-level parser
    #########################################
    parser = argparse.ArgumentParser(prog='poretools', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", help="Installed poretools version",
                        action="version",
                        version="%(prog)s " + str(poretools.version.__version__))
    subparsers = parser.add_subparsers(title='[sub-commands]', dest='command')

    #########################################
    # create the individual tool parsers
    #########################################

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
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev'],
                              default='all',
                              help='Which type of FASTA entries should be reported? Def.=all')
    parser_fastq.add_argument('--min-length',
                              dest='min_length',
                              default=0,
                              type=int,
                              help=('Minimum read length for FASTQ entry to be reported.'))
    parser_fastq.set_defaults(func=fastq.run)


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
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev'],
                              default='all',
                              help='Which type of FASTQ entries should be reported? Def.=all')
    parser_fasta.add_argument('--min-length',
                              dest='min_length',
                              default=0,
                              type=int,
                              help=('Minimum read length for FASTA entry to be reported.'))
    parser_fasta.set_defaults(func=fasta.run)


    ##########
    # stats
    ##########
    parser_stats = subparsers.add_parser('stats',
                                        help='Get read size stats for a set of FAST5 files')
    parser_stats.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_stats.set_defaults(func=stats.run)


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
    parser_hist.set_defaults(func=hist.run)


    ###########
    # events
    ###########
    parser_events = subparsers.add_parser('events',
                                        help='Extract each nanopore event for each read.')
    parser_events.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_events.set_defaults(func=events.run)

    
    ###########
    # readstats
    ###########
    parser_readstats = subparsers.add_parser('readstats',
                                        help='Extract signal information for each read over time.')
    parser_readstats.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_readstats.set_defaults(func=readstats.run)


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
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev'],
                              default='all',
                              help='Which type of FASTA entries should be reported? Def.=all')
    parser_tabular.set_defaults(func=tabular.run)

    
    #########
    # nucdist
    #########
    parser_nucdist = subparsers.add_parser('nucdist',
                                        help='Get the nucl. composition of a set of FAST5 files')
    parser_nucdist.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_nucdist.set_defaults(func=nucdist.run)

    
    ##########
    # qualdist
    ##########
    parser_qualdist = subparsers.add_parser('qualdist',
                                        help='Get the qual score composition of a set of FAST5 files')
    parser_qualdist.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_qualdist.set_defaults(func=qualdist.run)


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
                              choices=['all', 'fwd', 'rev', '2D', 'fwd,rev'],
                              default='all',
                              help='Which type of FASTA entries should be reported? Def.=all')
    parser_winner.set_defaults(func=winner.run)

    ###########
    # wiggle
    ###########
    parser_wiggle = subparsers.add_parser('wiggle',
                                        help='Create a wiggle plot of the observe signal for a FAST5 read.')
    parser_wiggle.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_wiggle.add_argument('--saveas',
                             dest='saveas',
                             metavar='STRING',
                             choices=['pdf', 'png'],
                             help='Save the wiggle plot to a file.',
                             default=None)
    parser_wiggle.set_defaults(func=wiggle.run)

    #######################################################
    # parse the args and call the selected function
    #######################################################
    args = parser.parse_args()

    try:
      args.func(parser, args)
    except IOError, e:
         if e.errno != 32:  # ignore SIGPIPE
             raise

if __name__ == "__main__":
    main()
