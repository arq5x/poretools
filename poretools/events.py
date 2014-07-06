import Fast5File

def run(parser, args):

	# print header.
	keys = ['file', 'strand', 'mean', 'start', 'stdv', \
			'length', 'model_state', 'model_level', 'move', \
			'p_model_state', 'mp_model_state', 'p_mp_model_state', \
			'p_A', 'p_C', 'p_G', 'p_T', 'raw_index']
	print "\t".join(keys)
	
	for fast5 in Fast5File.Fast5FileSet(args.files):

		for event in fast5.get_template_events():
			print '\t'.join([fast5.filename, 'template', str(event)]) 
		for event in fast5.get_complement_events():
			print '\t'.join([fast5.filename, 'complement', str(event)]) 

		fast5.close()

