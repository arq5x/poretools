import Fast5File
from collections import Counter

def run(parser, args):

	nuc_count = Counter()
	total_nucs = 0

	for fast5 in Fast5File.Fast5FileSet(args.files):
		fq = fast5.get_fastq()
		if fq is not None:
			for n in fq.seq:
				nuc_count[n] += 1
				total_nucs += 1
		fast5.close()

	for n in nuc_count:
		print '\t'.join(str(s) for s in [n, nuc_count[n], 
			total_nucs, float(nuc_count[n]) / float(total_nucs)])