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
		
		
		# run and flowcell parameters
		asic_temp  = fast5.get_asic_temp()
		asic_id = fast5.get_asic_id()
		heatsink_temp = fast5.get_heatsink_temp()
		channel_number = fast5.get_channel_number()
		
		start_time = None

		duration = None
		
		
		# sequence file info
		fast5_version = fast5.guess_version()
		
		# read info
		fastq_reads = fast5.get_fastqs('all')
		length_template = None
		length_complement = None
		length_2d = None
		if (len(fastq_reads) > 0):
			length_template = len(fastq_reads[0].seq)
		if (len(fastq_reads) > 2):
			length_complement = len(fastq_reads[1].seq)
			length_2d = len(fastq_reads[2].seq)

		print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
			fast5.filename,
			length_template,
			length_complement,
			length_2d,		
			asic_id, asic_temp, heatsink_temp,channel_number,start_time,duration,fast5_version)

		fast5.close()
