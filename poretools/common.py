import os
import glob
import sys

def get_fast5_files(file):

	# return as-is if list of files
	if len(file) > 1:
		return file

	# if just one "file" provided, assume it is a dir.
	dir = file[0]
	if os.path.isdir(dir):
		pattern = dir + '/' + '*.fast5'
		files = glob.glob(pattern)
		return files
	else:
		sys.stderr.write("Directory %s could not be opened. Exiting.\n" % dir)
		sys.exit()