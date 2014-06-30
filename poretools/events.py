import common
import Fast5File

def run(parser, args):

	# print header.
	keys = ['file', 'strand', 'mean', 'start', 'stdv', 'length', 'model_state', 'model_level', 'move', 'p_model_state', 'mp_model_state', 'p_mp_model_state', 'p_A', 'p_C', 'p_G', 'p_T', 'raw_index']
	print "\t".join(keys)
	
	for filename in common.get_fast5_files(args.files):
		fast5 = Fast5File.Fast5File(filename)

		for event in fast5.get_template_events():
			print '\t'.join([filename, 'template', str(event)]) 
		for event in fast5.get_complement_events():
			print '\t'.join([filename, 'complement', str(event)]) 

		fast5.close()

