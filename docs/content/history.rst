###############
Release History
###############

Version 0.6.0 (29-Aug-2016)
============================
0. Added new ``organise`` command to place FAST5 files into a useful folder hierarchy
1. Updated the logic for event timing to handle both R9 and earlier FAST5 files.
2. Added a "best" option to the ``fasta`` and ``fastq`` tools to identify the best sequence for a read (of 2d, template, complement).
3. Added R9 RNN support.
4. Various updates to API to accommodate the R9 changes made to the HDF5 structure.