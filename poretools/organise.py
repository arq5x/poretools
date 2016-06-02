import Fast5File
import sys
import os
from os import makedirs
import os.path
import shutil

#logging
import logging
logger = logging.getLogger('poretools')
logger.setLevel(logging.INFO)

def run(parser, args):
	if not os.path.isdir(args.dest):
                logger.error('destination directory needs to exist')
                return

	for fast5 in Fast5File.Fast5FileSet(args.files):

		offset = fast5.get_start_time() - fast5.get_exp_start_time()

		path = "%s/%s/%s/%s/%s" % (args.dest,
                                             fast5.get_host_name(),
                                             fast5.get_asic_id(),
                                             fast5.get_run_id(),
			        	     offset / 60 / 60)

		if not os.path.isdir(path):
			makedirs(path)

		#fas = fast5.get_fastas(args.type)

		fast5.close()

		filename = os.path.split(fast5.filename)[1]
		if args.copy:
			shutil.copyfile(fast5.filename, path + '/' + filename)
		else:
			shutil.move(fast5.filename, path + '/' + filename)

