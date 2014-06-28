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
	git clone https://github.com/arq5x/poretools
	cd poretools
    python setup.py install
    # or
    sudo python setup.py install


Examples
========

Extract sequences in FASTQ format from a set of FAST5 files.

    poretools fastq fast5/*.fast5

Or, if there are too many files for your OS to do the wildcard expansion, just provide a directory.
``poreutils`` will automatically find all of the FAST5 files in the directory.

    poretools fastq fast5/*.fast5


Extract sequences in FASTQ format from a set of FAST5 files.
    
    poretools fastq fast5/*.fast5
    poretools fastq --min-length 5000 fast5/*.fast5
    poretools fastq --type all fast5/*.fast5
    poretools fastq --type fwd fast5/*.fast5
    poretools fastq --type rev fast5/*.fast5
    poretools fastq --type 2D fast5/*.fast5
    poretools fastq --type fwd,rev fast5/*.fast5


Extract sequences in FASTA format from a set of FAST5 files.
    
    poretools fasta fast5/*.fast5
    poretools fasta --min-length 5000 fast5/*.fast5
    poretools fasta --type all fast5/*.fast5
    poretools fasta --type fwd fast5/*.fast5
    poretools fasta --type rev fast5/*.fast5
    poretools fasta --type 2D fast5/*.fast5
    poretools fasta --type fwd,rev fast5/*.fast5

Collect read size statistics from a set of FAST5 files.
    
    poretools stats fast5/*.fast5

Plot a histogram of read sizes from a set of FAST5 files.
    
    poretools hist fast5/*.fast5
    poretools hist --min-length 1000 --max-length 10000 fast5/*.fast5
    poretools hist --num-bins 20 --max-length 10000 fast5/*.fast5

Look at the nucleotide composition of a set of FAST5 files.
    
    poretools nucdist fast5/*.fast5

Look at the quality score composition of a set of FAST5 files.
    
    poretools qualdist fast5/*.fast5
