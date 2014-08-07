##########
Options
##########

The following demonstrates the options available in ``poretools``.

.. code-block:: bash

    poretools --help
    usage: poretools [-h] [-v]

                     {combine,fastq,fasta,stats,hist,events,readstats,tabular,nucdist,qualdist,winner,wiggle,times}
                     ...

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Installed poretools version

    [sub-commands]:
      {combine,fastq,fasta,stats,hist,events,readstats,tabular,nucdist,qualdist,winner,wiggle,times}
        combine             Combine a set of FAST5 files in a TAR achive
        fastq               Extract FASTQ sequences from a set of FAST5 files
        fasta               Extract FASTA sequences from a set of FAST5 files
        stats               Get read size stats for a set of FAST5 files
        hist                Plot read size histogram for a set of FAST5 files
        events              Extract each nanopore event for each read
        readstats           Extract signal information for each read over time.
        tabular             Extract the lengths and name/seq/quals from a set of
                            FAST5 files in TAB delimited format
        nucdist             Get the nucl. composition of a set of FAST5 files
        qualdist            Get the qual score composition of a set of FAST5 files
        winner              Get the longest read from a set of FAST5 files
        squiggle            Plot the observed signals for FAST5 reads
        times               Return the start times from a set of FAST5 files in
                            tabular format
        yield_plot          Plot the yield over time for a set of FAST5 files