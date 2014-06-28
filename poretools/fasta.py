import common
import Fast5File

def run(parser, args):
	
	for filename in common.get_fast5_files(args.files):
		fast5 = Fast5File.Fast5File(filename)
		fas = fast5.get_fastas(args.type)

		for fa in fas:
			if fa is None or \
			len(fa.seq) < args.min_length:			
				fast5.close()
				continue
			
			print fa
		fast5.close()

