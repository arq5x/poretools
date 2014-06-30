import common
import Fast5File

def run(parser, args):
	
	print '\t'.join(['length', 'name', 'sequence', 'quals'])
	
	for filename in common.get_fast5_files(args.files):
		fast5 = Fast5File.Fast5File(filename)
		fqs = fast5.get_fastqs(args.type)
		for fq in fqs:
			if fq is None:
				fast5.close()
				continue
			print '\t'.join([str(len(fq.seq)), fq.name, fq.seq, fq.qual])
		fast5.close()