import sys
import matplotlib.pyplot as plt
import Fast5File

def run(parser, args):
	sizes = []
	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		fq = fast5.get_fastq()
		if fq is not None:
			sizes.append(len(fq.seq))
		fast5.close()

	print sizes 
	n, bins, patches = \
		plt.hist([s for s in sizes if s < args.max_length and s > args.min_length], 
				 args.num_bins, facecolor='green', alpha=0.75)
	plt.xlabel('Read length')
	plt.ylabel('Count')
	plt.show()#