import Fast5File

def run(parser, args):

	for fast5 in Fast5File.Fast5FileSet(args.files):

		start_time = fast5.get_start_time()
		channel_number = fast5.get_channel_number()
		read_number = fast5.get_read_number()

		template_len = 0
		if fast5.get_template_events() is not None:
			template_len = len(fast5.get_template_events())
		complement_len = 0
		if fast5.get_complement_events() is not None:
			complement_len = len(fast5.get_complement_events())

		print "%s\t%s\t%s\t%s\t%s" % (start_time, channel_number, read_number, template_len, complement_len)

		fast5.close()