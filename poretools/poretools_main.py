#!/usr/bin/env python

import os.path
import sys
import argparse

# poretools imports
import stats
import hist
import fasta
import fastq
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

    # stats
    parser_stats = subparsers.add_parser('stats',
                                        help='Get read size stats for a set of FAST5 files')
    parser_stats.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_stats.set_defaults(func=stats.run)

    # hist
    parser_hist = subparsers.add_parser('hist',
                                        help='Plot read size histogram for a set of FAST5 files')
    parser_hist.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_hist.set_defaults(func=hist.run)

    # FASTA
    parser_fasta = subparsers.add_parser('fasta',
                                        help='Extract FASTA sequences from a set of FAST5 files')
    parser_fasta.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_fasta.set_defaults(func=fasta.run)

    # FASTQ
    parser_fastq = subparsers.add_parser('fastq',
                                        help='Extract FASTQ sequences from a set of FAST5 files')
    parser_fastq.add_argument('files', metavar='FILES', nargs='+',
                             help='The input FAST5 files.')
    parser_fastq.set_defaults(func=fastq.run)

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
