import Fast5File
import datetime

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

	print "source_filename\ttemplate_fwd_length\tcomplement_rev_length\t2d_length\tasic_id\tasic_temp\theatsink_temp\tchannel\texp_start_time\texp_start_time_string_date\texp_start_time_string_time\tstart_time\tstart_time_string_date\tstart_time_string_time\tduration\tfast5_version"

	for fast5 in Fast5File.Fast5FileSet(args.files):
		
		
		# run and flowcell parameters
		asic_temp  = fast5.get_asic_temp()
		asic_id = fast5.get_asic_id()
		heatsink_temp = fast5.get_heatsink_temp()
		channel_number = fast5.get_channel_number()
		
		# try and get timing info
		try:
			start_time = fast5.get_start_time()
			start_time_string = datetime.datetime.fromtimestamp(float(start_time)).strftime("%Y-%b-%d (%a)\t%H:%M:%S")
			exp_start_time = fast5.get_exp_start_time()
			exp_start_time_string = datetime.datetime.fromtimestamp(float(exp_start_time)).strftime("%Y-%b-%d (%a)\t%H:%M:%S")
			duration = fast5.get_duration()
		except KeyError:	
			start_time = "Not found"
			start_time_string = "NA\tNA"
			exp_start_time = "Not found"
			exp_start_time_string = "NA\tNA"
			duration = "Not found"
		
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

		print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
			fast5.filename,
			length_template,
			length_complement,
			length_2d,		
			asic_id, asic_temp, heatsink_temp,channel_number,exp_start_time,exp_start_time_string,start_time,start_time_string,duration,fast5_version)

		fast5.close()
