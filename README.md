A wee toolkit for working with nanopore sequencing data from Oxford Nanopore.

Requirements
============
- Python 2.7+
- hd5f
- Pytables 3.x
- NUMPY
- Matplotlib

Installation
========
    python setup.py install

Examples
========

Extract sequences in FASTQ format from a set of FAST5 files.
    
    poretools fastq fast5/*.fast5

Extract sequences in FASTA format from a set of FAST5 files.
    
    poretools fasta fast5/*.fast5

Collect read size statistics from a set of FAST5 files.
    
    poretools stats fast5/*.fast5

Plot a histogram of read sizes from a set of FAST5 files.
    
    poretools hist fast5/*.fast5