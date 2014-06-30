import os
import glob
import sys

def get_fast5_files(file):

	# return as-is if list of files
	if len(file) > 1:
		return file
	elif len(file) == 1:
		# e.g. ['/path/to/dir'] or ['/path/to/file']
		file = file[0]
		# is it a directory or single file?
		if os.path.isdir(file):
			pattern = file + '/' + '*.fast5'
			files = glob.glob(pattern)
			return files
		else:
			return [file]
	else:
		sys.stderr.write("Directory %s could not be opened. Exiting.\n" % dir)
		sys.exit()
