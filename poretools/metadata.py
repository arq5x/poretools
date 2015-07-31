import Fast5File

def run(parser, args):

	if args.read:
		for i, fast5 in enumerate(Fast5File.Fast5FileSet(args.files)):
			for metadata_dict in fast5.read_metadata:
				if i == 0:
					header = metadata_dict.keys()
					print "\t".join(["filename"] + header)
				print "\t".join([fast5.filename] + [str( metadata_dict[k] ) for k in header])
	else:
		print "asic_id\tasic_temp\theatsink_temp"
		for fast5 in Fast5File.Fast5FileSet(args.files):

			asic_temp  = fast5.get_asic_temp()
			asic_id = fast5.get_asic_id()
			heatsink_temp = fast5.get_heatsink_temp()

			print "%s\t%s\t%s" % (asic_id, asic_temp, heatsink_temp)

			fast5.close()
