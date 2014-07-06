import Fast5File

def run(parser, args):

	for fast5 in Fast5File.Fast5FileSet(args.files):
		fqs = fast5.get_fastqs(args.type)
		for fq in fqs:
			if fq is None or \
			len(fq.seq) < args.min_length:			
				fast5.close()
				continue
			
			print fq
		fast5.close()
