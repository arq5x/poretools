import Fast5File

def run(parser, args):
	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		fq = fast5.fastq
		if fq is not None:
			print fq
		fast5.close()
