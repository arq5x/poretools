import sys
import tables as pyhdf5
import formats
from Event import Event

fastq_paths = {'template' : '/Analyses/Basecall_2D_000/BaseCalled_template',
               'complement' : '/Analyses/Basecall_2D_000/BaseCalled_complement',
               'twodirections' : '/Analyses/Basecall_2D_000/BaseCalled_2D'}

class Fast5File(object):

	def __init__(self, filename):
		self.filename = filename
		self.open()

		self.fastas = {}
		self.fastqs = {}
		
		self._extract_fastqs_from_fast5()
		self._extract_fastas_from_fast5()
		self._extract_template_events()
		self._extract_complement_events()

		self._get_metadata()

	####################################################################
	# Public API methods
	####################################################################

	def open(self):
		"""
		Open an ONT Fast5 file, assuming HDF5 format
		"""
		self.hdf5file = pyhdf5.open_file(self.filename, 'r')

	def close(self):
		"""
		Close an open an ONT Fast5 file, assuming HDF5 format
		"""
		self.hdf5file.close()

	def get_fastqs(self, choice):
		"""
		Return the set of base called sequences in the FAST5
		in FASTQ format.
		"""
		# TODO "best". What is "best"?
		fqs = []
		if choice == "all":
			for fastq in self.fastqs:
				fqs.append(self.fastqs[fastq])
		elif choice == "fwd":
				fqs.append(self.fastqs.get('template'))
		elif choice == "rev":
				fqs.append(self.fastqs.get('complement'))
		elif choice == "2D":
				fqs.append(self.fastqs.get('twodirections'))
		elif choice == "fwd,rev":
				fqs.append(self.fastqs.get('template'))
				fqs.append(self.fastqs.get('complement'))

		return fqs


	def get_fastas(self, choice):
		"""
		Return the set of base called sequences in the FAST5
		in FASTQ format.
		"""
		# TODO "best". What is "best"?
		fas = []
		if choice == "all":
			for fasta in self.fastas:
				fas.append(self.fastas[fasta])
		elif choice == "fwd":
				fas.append(self.fastas.get('template'))
		elif choice == "rev":
				fas.append(self.fastas.get('complement'))
		elif choice == "2D":
				fas.append(self.fastas.get('twodirections'))
		elif choice == "fwd,rev":
				fas.append(self.fastas.get('template'))
				fas.append(self.fastas.get('complement'))

		return fas


	def get_fastq(self):
		"""
		Return the base called sequence in the FAST5
		in FASTQ format. Try 2D then template, then complement.
		If all fail, return None
		"""
		if not self.fastqs:
			return None
		elif self.fastqs.get('twodirections') is not None:
			return self.fastqs.get('twodirections')
		elif self.fastqs.get('template') is not None:
			return self.fastqs.get('template')
		elif self.fastqs.get('complement') is not None:
			return self.fastqs.get('complement')


	def get_fasta(self):
		"""
		Return the base called sequence in the FAST5
		in FASTA format. Try 2D then template, then complement.
		If all fail, return None
		"""
		if not self.fastas:
			return None
		elif self.fastas.get('twodirections') is not None:
			return self.fastas.get('twodirections')
		elif self.fastas.get('template') is not None:
			return self.fastas.get('template')
		elif self.fastas.get('complement') is not None:
			return self.fastas.get('complement')

	def get_template_events(self):
		"""
		Return the table of event data for the template strand
		"""
		return self.template_events

	def get_complement_events(self):
		"""
		Return the table of event data for the complement strand
		"""
		return self.complement_events

	####################################################################
	# Flowcell Metadata methods
	####################################################################

	def get_start_time(self):
		"""
		Return the starting time at which signals were collected
		for the given read.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('exp_start_time')
		except:
			return None

	def get_channel_number(self):
		"""
		Return the channel (pore) number at which signals were collected
		for the given read.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('channel_number')
		except:
			return None

	def get_read_number(self):
		"""
		Return the read number for the pore representing the given read.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('read_number')
		except:
			return None

	def get_version_name(self):
		"""
		Return the flow cell version name.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('version_name')
		except:
			return None

	def get_run_id(self):
		"""
		Return the run id.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('run_id')
		except:
			return None

	def get_heatsink_temp(self):
		"""
		Return the heatsink temperature.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('heatsink_temp')
		except:
			return None

	def get_asic_temp(self):
		"""
		Return the ASIC temperature.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('asic_temp')
		except:
			return None

	def get_flowcell_id(self):
		"""
		Return the flowcell_id.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('flowcell_id')
		except:
			return None

	def get_run_purpose(self):
		"""
		Return the exp_script_purpose.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('exp_script_purpose')
		except:
			return None

	def get_asic_id(self):
		"""
		Return the flowcell's ASIC id.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('asic_id')
		except:
			return None

	def get_device_id(self):
		"""
		Return the flowcell's device id.
		"""
		try:
			return self.keyinfo.tracking_id._f_getAttr('device_id')
		except:
			return None

	####################################################################
	# Private API methods
	####################################################################

	def _extract_fastqs_from_fast5(self):
		"""
		Return the sequence in the FAST5 file in FASTQ format
		"""
		for id, h5path in fastq_paths.iteritems(): 
			try:
				table = self.hdf5file.getNode(h5path)
				fq = formats.Fastq(table.Fastq[()])
				fq.name += "_" + id + ":" + self.filename
				self.fastqs[id] = fq
			except Exception, e:
				pass

	def _extract_fastas_from_fast5(self):
		"""
		Return the sequence in the FAST5 file in FASTA format
		"""
		for id, h5path in fastq_paths.iteritems(): 
			try:
				table = self.hdf5file.getNode(h5path)
				fa = formats.Fasta(table.Fastq[()])
				fa.name += "_" + id + " " + self.filename
				self.fastas[id] = fa
			except Exception, e:
				pass

	def _extract_template_events(self):
		"""
		Pull out the event information for the template strand
		"""
		try:
			table = self.hdf5file.getNode(fastq_paths['template'])
			self.template_events = [Event(x) for x in table.Events]
		except Exception, e:
			self.template_events = []

	def _extract_complement_events(self):
		"""
		Pull out the event information for the complementary strand
		"""
		try:
			table = self.hdf5file.getNode(fastq_paths['complement'])
			self.complement_events = [Event(x) for x in table.Events]
		except Exception, e:
			self.complement_events = []

	def _get_metadata(self):
		try:
			self.keyinfo = self.hdf5file.getNode('/UniqueGlobalKey')
		except Exception, e:
			try:
				self.keyinfo = self.hdf5file.getNode('/Key')
			except Exception, e:
				self.keyinfo = None
				sys.stderr.write("Cannot find keyinfo. Exiting.\n")
