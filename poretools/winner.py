import Fast5File
import sys

#logging
import logging
logger = logging.getLogger('poretools')


def run(parser, args):
	longest_size = 0
	longest_read = None
	
	for fast5 in Fast5File.Fast5FileSet(args.files):
		fas = fast5.get_fastas(args.type)

		for fa in fas:
			if fa and len(fa.seq) > longest_size:
				longest_size = len(fa.seq)
				longest_read = fa

		fast5.close()

	logger.info("Wow, it's a whopper: your longest read is %d bases." % (longest_size,))
	print longest_read

