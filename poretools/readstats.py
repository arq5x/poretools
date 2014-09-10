import Fast5File

def run(parser, args):

	print "start_time\tchannel_number\tread_number\ttemplate_events\tcomplement_events"

	for fast5 in Fast5File.Fast5FileSet(args.files):

		start_time = fast5.get_start_time()
		channel_number = fast5.get_channel_number()
		read_number = fast5.get_read_number()

		template_events = fast5.get_template_events()
		if template_events is not None:
			template_len = len(template_events)
		else:
			template_len = 0

		complement_events = fast5.get_complement_events()
		if complement_events is not None:
			complement_len = len(complement_events)
		else:
			complement_len = 0

		print "%s\t%s\t%s\t%s\t%s" % (start_time, channel_number, read_number, template_len, complement_len)

		fast5.close()
