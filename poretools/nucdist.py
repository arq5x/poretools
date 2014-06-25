import Fast5File
from collections import Counter

def run(parser, args):

	nuc_count = Counter()
	total_nucs = 0

	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		if fast5.fastq is not None:
			for n in fast5.fastq.seq:
				nuc_count[n] += 1
				total_nucs += 1
		fast5.close()

	for n in nuc_count:
		print '\t'.join(str(s) for s in [n, nuc_count[n], 
			total_nucs, float(nuc_count[n]) / float(total_nucs)])