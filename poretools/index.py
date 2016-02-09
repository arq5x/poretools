import Fast5File

############
#
#	index
#
#   A tool to extract
#	all info needed to 
#	identify a pile of 
#	unsorted reads from 
#	multiple MinION
#	sequencing 
#	experiments.
#
############

def run(parser, args):

	print "asic_id\tasic_temp\theatsink_temp"

	for fast5 in Fast5File.Fast5FileSet(args.files):

		asic_temp  = fast5.get_asic_temp()
		asic_id = fast5.get_asic_id()
		heatsink_temp = fast5.get_heatsink_temp()

		print "%s\t%s\t%s" % (asic_id, asic_temp, heatsink_temp)

		fast5.close()
