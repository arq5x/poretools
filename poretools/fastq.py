import Fast5File

def run(parser, args):
	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		
		fq = fast5.fastq
		if fq is not None:

			# does the read meet user's criteria?
			if len(fq.seq) < args.min_length:
				fast5.close()
				continue
			print fq
		
		fast5.close()
