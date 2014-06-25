import Fast5File

def run(parser, args):
	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		if fast5.fasta is not None:
			print fast5.fasta
		fast5.close()
