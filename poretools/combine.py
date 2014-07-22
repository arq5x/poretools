import tarfile
import sys
import Fast5File

#logging
import logging
logger = logging.getLogger('poretools')


def run(parser, args):
	
	if args.tar_filename.endswith('.tar'):
		tar = tarfile.open(args.tar_filename, mode='w')
	elif args.tar_filename.endswith('.gz'):
		tar = tarfile.open(args.tar_filename, mode='w:gz')
	elif args.tar_filename.endswith('.bz2'):
		tar = tarfile.open(args.tar_filename, mode='w:bz2')
	else:
		logger.error("Unrecognized FAST5 archive extension. Exiting.\n")
		sys.exit()

	file_count = 0
	for fast5 in Fast5File.Fast5FileSet(args.files):
		tar.add(fast5.filename)
		fast5.close()
		file_count += 1
	tar.close()

	logger.info("%s successfully created from %d FAST5 files.\n" % \
		(args.tar_filename, file_count))
