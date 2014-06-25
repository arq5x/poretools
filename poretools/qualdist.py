import Fast5File
from collections import Counter

def run(parser, args):

	qual_count = Counter()
	total_nucs = 0

	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		if fast5.fastq is not None:
			for q in fast5.fastq.qual:
				qual_count[q] += 1
				total_nucs += 1
		fast5.close()

	for q in qual_count:
		print '\t'.join(str(s) for s in [q, ord(q)-33, qual_count[q], 
			total_nucs, float(qual_count[q]) / float(total_nucs)])