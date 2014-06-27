import Fast5File

def run(parser, args):
	for filename in args.files:
		fast5 = Fast5File.Fast5File(filename)
		
		fa = fast5.fasta
		if fa is not None:

			# does the read meet user's criteria?
			if len(fa.seq) < args.min_length:
				fast5.close()
				continue

			print fa

		fast5.close()
