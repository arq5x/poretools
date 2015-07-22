import sys
import os
import glob
import tarfile
import shutil
import h5py
from watchdog.events import RegexMatchingEventHandler

#logging
import logging
logger = logging.getLogger('poretools')


# poretools imports
import formats
from Event import Event

fastq_paths = {'template' : '/Analyses/Basecall_2D_000/BaseCalled_template',
               'complement' : '/Analyses/Basecall_2D_000/BaseCalled_complement',
               'twodirections' : '/Analyses/Basecall_2D_000/BaseCalled_2D',
               'pre_basecalled' : '/Analyses/EventDetection_000/Reads/'}

FAST5SET_FILELIST = 0
FAST5SET_DIRECTORY = 1
FAST5SET_SINGLEFILE = 2
FAST5SET_TARBALL = 3
PORETOOLS_TMPDIR = '.poretools_tmp'


class Fast5DirHandler(RegexMatchingEventHandler):

    patterns = ["*.fast5"]

    def __init__(self, dir):
        self.dir = dir
        self.files = []
        super(Fast5DirHandler, self).__init__()

        if os.path.isdir(self.dir):
            pattern = self.dir + '/' + '*.fast5'
            files = glob.glob(pattern)
            self.files = files

    def process(self, event):
        self.files.append(event.src_path)

    def on_created(self, event):
        self.process(event)

    def clear(self):
        self.files = []

    def __iter__(self):
        return self

    def next(self):
        if len(self.files) > 0:
            return self.files.pop(0)
        else:
            raise StopIteration()


class Fast5FileSet(object):

	def __init__(self, fileset):
		if isinstance(fileset, list):
			self.fileset = fileset
		elif isinstance(fileset, str):
			self.fileset = [fileset]
		self.set_type = None
		self.num_files_in_set = None
		self._extract_fast5_files()

	def get_num_files(self):
		"""
		Return the number of files in the FAST5 set.
		"""
		if self.num_files_in_set is None and self.set_type == FAST5SET_TARBALL:
			self.num_files_in_set = len(self.files)
		return self.num_files_in_set

	def __iter__(self):
		return self

	def next(self):
		try:
			return Fast5File(self.files.next())
		except Exception as e:
			# cleanup our mess
			if self.set_type == FAST5SET_TARBALL:
				shutil.rmtree(PORETOOLS_TMPDIR)
			raise StopIteration

	def _extract_fast5_files(self):

		# return as-is if list of files
		if len(self.fileset) > 1:
			self.files = iter(self.fileset)
			self.num_files_in_set = len(self.fileset)
			self.set_type = FAST5SET_FILELIST
		elif len(self.fileset) == 1:
			# e.g. ['/path/to/dir'] or ['/path/to/file']
			f = self.fileset[0]
			# is it a directory?
			if os.path.isdir(f):
				pattern = f + '/' + '*.fast5'
				files = glob.glob(pattern)
				self.files = iter(files)
				self.num_files_in_set = len(files)
				self.set_type = FAST5SET_DIRECTORY
				if not len(files):
					logger.warning("Directory is empty!")

			# is it a tarball?
			elif tarfile.is_tarfile(f):
				if os.path.isdir(PORETOOLS_TMPDIR):
					shutil.rmtree(PORETOOLS_TMPDIR)
				os.mkdir(PORETOOLS_TMPDIR)

				self.files = TarballFileIterator(f)
				# set to None to delay initialisation
				self.num_files_in_set = None
				self.set_type = FAST5SET_TARBALL

			# just a single FAST5 file.
			else:
				self.files = iter([f])
				self.num_files_in_set = 1
				self.set_type = FAST5SET_SINGLEFILE
		else:
			logger.error("Directory %s could not be opened. Exiting.\n" % dir)
			sys.exit()

class TarballFileIterator:
	def _fast5_filename_filter(self, filename):
		return os.path.basename(filename).endswith('.fast5') and not os.path.basename(filename).startswith('.')

	def __init__(self, tarball):
		self._tarball = tarball
		self._tarfile = tarfile.open(tarball)

	def __del__(self):
		self._tarfile.close()

	def __iter__(self):
		return self

	def next(self):
		while True:
			tarinfo = self._tarfile.next()
			if tarinfo is None:
				raise StopIteration
			elif self._fast5_filename_filter(tarinfo.name):
				break
		self._tarfile.extract(tarinfo, path=PORETOOLS_TMPDIR)
		return os.path.join(PORETOOLS_TMPDIR, tarinfo.name)

	def __len__(self):
		with tarfile.open(self._tarball) as tar:
			return len(tar.getnames())


class Fast5File(object):

	def __init__(self, filename):
		self.filename = filename
		self.is_open = self.open()

		self.fastas = {}
		self.fastqs = {}
		
		# pre-load the FASTQ data
		#self._extract_fastqs_from_fast5()

		# booleans for lazy loading (speed)
		self.have_fastqs = False
		self.have_fastas = False
		self.have_templates = False
		self.have_complements = False
		self.have_pre_basecalled = False
		self.have_metadata = False

	def __del__(self):
		self.close()

	####################################################################
	# Public API methods
	####################################################################

	def open(self):
		"""
		Open an ONT Fast5 file, assuming HDF5 format
		"""
		try:
			self.hdf5file = h5py.File(self.filename, 'r')
			return True
		except Exception, e:
			logger.warning("Cannot open file: %s. Perhaps it is corrupt? Moving on.\n" % self.filename)
			return False
			
	def close(self):
		"""
		Close an open an ONT Fast5 file, assuming HDF5 format
		"""
		if self.is_open:
			self.hdf5file.close()
			self.is_open = False

	def has_2D(self):
		"""
		Return TRUE if the FAST5 has a 2D base-called sequence.
		Return FALSE otherwise.
		"""
		if self.have_fastas is False:
			self._extract_fastas_from_fast5()
			self.have_fastas = True

		if self.fastas.get('twodirections') is not None:
			return True
		return False

	def get_fastqs(self, choice):
		"""
		Return the set of base called sequences in the FAST5
		in FASTQ format.
		"""
		if self.have_fastqs is False:
			self._extract_fastqs_from_fast5()
			self.have_fastqs = True

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
		if self.have_fastas is False:
			self._extract_fastas_from_fast5()
			self.have_fastas = True

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

	def get_fastas_dict(self):
                """
                Return the set of base called sequences in the FAST5
                in FASTQ format.
                """
                if self.have_fastas is False:
                        self._extract_fastas_from_fast5()
                        self.have_fastas = True

		return self.fastas

	def get_fastq(self):
		"""
		Return the base called sequence in the FAST5
		in FASTQ format. Try 2D then template, then complement.
		If all fail, return None
		"""
		if self.have_fastqs is False:
			self._extract_fastqs_from_fast5()
			self.have_fastqs = True

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
		if self.have_templates is False:
			self._extract_template_events()
			self.have_templates = True

		return self.template_events

	def get_complement_events(self):
		"""
		Return the table of event data for the complement strand
		"""
		if self.have_complements is False:
			self._extract_complement_events()
			self.have_complements = True
		
		return self.complement_events

	def get_pre_basecalled_events(self):
		"""
		Return the table of pre-basecalled events
		"""
		if self.have_pre_basecalled is False:
			self._extract_pre_basecalled_events()
			self.have_pre_basecalled = True

		return self.pre_basecalled_events		

	####################################################################
	# Flowcell Metadata methods
	####################################################################

	def get_exp_start_time(self):
		"""
		Return the starting time at which signals were collected
		for the given read.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['exp_start_time']
		except:
			return None

	def get_channel_number(self):
		"""
		Return the channel (pore) number at which signals were collected
		for the given read.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['channel_id'].attrs['channel_number']
		except:
			pass

		try:
			return self.keyinfo['read_id'].attrs['channel_number']
		except:
			return None

	def find_read_number_block(self):
		path = "/Analyses/Basecall_2D_000"
		basecall = self.hdf5file[path]
		path = basecall.get('InputEvents', getlink=True)

		# the soft link target seems broken?
		newpath = "/" + "/".join(path.path.split("/")[:-1])

		node = self.hdf5file[newpath]

		return node

	def find_event_timing_block(self):
		path = "/Analyses/Basecall_2D_000/BaseCalled_template"
		try:
			node = self.hdf5file[path]
			path = node.get('Events')
#, getlink=True)
			return path
		except Exception:
			return None

	def get_read_number(self):
		"""
		Return the read number for the pore representing the given read.
		"""
		node = self.find_read_number_block()
		if node:
			try:
				return node.attrs['read_number']
			except:
				return None
		return None

	def get_duration(self):
		node = self.find_event_timing_block()
		if node:
			return int(node.attrs['duration'])
		return None

	def get_start_time(self):
		exp_start_time	= self.get_exp_start_time()
	
		node = self.find_event_timing_block()
		if node:
			return int(exp_start_time) + int(node.attrs['start_time'])
	
		return None

	def get_end_time(self):
		exp_start_time	= self.get_exp_start_time()
		start_time = self.get_start_time()
		duration = self.get_duration()

		if start_time and duration:
			return start_time + duration
		else:
			return None

	def get_version_name(self):
		"""
		Return the flow cell version name.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['version_name']
		except:
			return None

	def get_run_id(self):
		"""
		Return the run id.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['run_id']
		except:
			return None

	def get_heatsink_temp(self):
		"""
		Return the heatsink temperature.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['heatsink_temp']
		except:
			return None

	def get_asic_temp(self):
		"""
		Return the ASIC temperature.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['asic_temp']
		except:
			return None

	def get_flowcell_id(self):
		"""
		Return the flowcell_id.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['flowcell_id']
		except:
			return None

	def get_run_purpose(self):
		"""
		Return the exp_script_purpose.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['exp_script_purpose']
		except:
			return None

	def get_asic_id(self):
		"""
		Return the flowcell's ASIC id.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['asic_id']
		except:
			return None

		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

	def get_device_id(self):
		"""
		Return the flowcell's device id.
		"""
		try:
			return self.keyinfo['tracking_id'].attrs['device_id']
		except:
			return None


	def get_template_events_count(self):
		"""
		Pull out the event count for the template strand
		"""
		try:
			table = self.hdf5file[fastq_paths['template']]
			return len(table['Events'][()])
		except Exception, e:
			return 0

	def get_complement_events_count(self):
		"""
		Pull out the event count for the complementary strand
		"""
		try:
			table = self.hdf5file[fastq_paths['complement']]
			return len(table['Events'][()])
		except Exception, e:
			return 0

	def is_high_quality(self):
		if self.get_complement_events_count() >= \
		   self.get_template_events_count():
			return True
		else:
			return False

	####################################################################
	# Private API methods
	####################################################################

	def _extract_fastqs_from_fast5(self):
		"""
		Return the sequence in the FAST5 file in FASTQ format
		"""
		for id, h5path in fastq_paths.iteritems(): 
			try:
				table = self.hdf5file[h5path]
				fq = formats.Fastq(table['Fastq'][()])
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
				table = self.hdf5file[h5path]
				fa = formats.Fasta(table['Fastq'][()])
				fa.name += "_" + id + " " + self.filename
				self.fastas[id] = fa
			except Exception, e:
				pass

	def _extract_template_events(self):
		"""
		Pull out the event information for the template strand
		"""
		try:
			table = self.hdf5file[fastq_paths['template']]
			self.template_events = [Event(x) for x in table['Events'][()]]
		except Exception, e:
			self.template_events = []

	def _extract_complement_events(self):
		"""
		Pull out the event information for the complementary strand
		"""
		try:
			table = self.hdf5file[fastq_paths['complement']]
			self.complement_events = [Event(x) for x in table['Events'][()]]
		except Exception, e:
			self.complement_events = []

	def _extract_pre_basecalled_events(self):
		"""
		Pull out the pre-basecalled event information 
		"""
		# try:
		table = self.hdf5file[fastq_paths['pre_basecalled']]
		events = []
		for read in table:
			events.extend(table[read]["Events"][()])
		self.pre_basecalled_events = [Event(x) for x in events]
		# except Exception, e:
			# self.pre_basecalled_events = []			

	def _get_metadata(self):
		try:
			self.keyinfo = self.hdf5file['/UniqueGlobalKey']
		except Exception, e:
			try:
				self.keyinfo = self.hdf5file['/Key']
			except Exception, e:
				self.keyinfo = None
				logger.warning("Cannot find keyinfo. Exiting.\n")
