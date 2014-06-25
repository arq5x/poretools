A wee toolkit for working with nanopore sequencing data from Oxford Nanopore.

Requirements
============
- Pytables 3.x
- NUMPY
- Matplotlib

Examples
========

1. Extract sequences in FASTQ format from a set of FAST5 files.
    
    poretools fastq fast5/*.fast5

2. Extract sequences in FASTA format from a set of FAST5 files.
    
    poretools fasta fast5/*.fast5

3. Collect read size statistics from a set of FAST5 files.
    
    poretools stats fast5/*.fast5

4. Plot a histogram of read sizes from a set of FAST5 files.
    
    poretools hist fast5/*.fast5