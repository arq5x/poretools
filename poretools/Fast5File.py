import sys
import os
import glob
import tarfile
import zipfile
import shutil
import h5py
import tempfile
import dateutil.parser
import datetime
import time

#logging
import logging
logger = logging.getLogger('poretools')

### Some notes on nanopore FAST5 file format:
### start_time used to be represented in seconds, when stored in the /Analyses subdirectories.
### more recently with MinKNOW updates start_time is stored as number of samples under /Reads/Raw
### and must be converted to seconds by dividing by sample frequency.

# poretools imports
import formats
from Event import Event

fastq_paths = {
  'closed' : {},
  'r9rnn' :         { 'template' : '/Analyses/Basecall_RNN_1D_%03d/BaseCalled_template'},
  'metrichor1.16' : { 'template' : '/Analyses/Basecall_1D_%03d/BaseCalled_template',
                      'complement' : '/Analyses/Basecall_1D_%03d/BaseCalled_complement',
                      'twodirections' : '/Analyses/Basecall_2D_%03d/BaseCalled_2D',
                      'pre_basecalled' : '/Analyses/EventDetection_000/Reads/'
                    },
  'classic' :       { 'template' : '/Analyses/Basecall_2D_%03d/BaseCalled_template',
                      'complement' : '/Analyses/Basecall_2D_%03d/BaseCalled_complement',
                      'twodirections' : '/Analyses/Basecall_2D_%03d/BaseCalled_2D',
                      'pre_basecalled' : '/Analyses/EventDetection_000/Reads/'
                    },
  'prebasecalled' : {'pre_basecalled' : '/Analyses/EventDetection_000/Reads/'}
}

FAST5SET_FILELIST = 0
FAST5SET_DIRECTORY = 1
FAST5SET_SINGLEFILE = 2
FAST5SET_TARBALL = 3
FAST5SET_ZIP = 4
PORETOOLS_TMPDIR = None
for testdir in ['/dev/shm/', '/tmp/', '.']:
	if os.path.isdir(testdir):
		PORETOOLS_TMPDIR = testdir
		break

class Fast5DirHandler(object):

    patterns = ["*.fast5"]

    def __init__(self, dir):
        self.dir = dir
        self.files = []
        super(Fast5DirHandler, self).__init__()

        
        if os.path.isdir(self.dir):
            pattern = self.dir + os.path.sep + '*.fast5'
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

	def __init__(self, fileset, group=0):
		self.set_type = None
		if isinstance(fileset, list):
			self.fileset = fileset
		elif isinstance(fileset, str):
			self.fileset = [fileset]
		else:
			raise Exception('unknown fileset - should be a string file path or list: %s'%(fileset))
		self.set_type = None
		self.num_files_in_set = None
		self.group = group
		self._tmp = tempfile.mkdtemp(prefix=PORETOOLS_TMPDIR)
		self.oldfiles = None
		self._extract_fast5_files()

	def __del__(self):
		if self._tmp:
			os.rmdir(self._tmp)

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
			# allow multiple tarball or zip files to expand
			try:
				nextFile = next(self.files)
			except StopIteration as e:
				if self.oldfiles:
					self.files = self.oldfiles;
					self.oldfiles = None;
					return self.next() # recurse
				else:
					raise e
				
			nextFast5 = None
			(f, ext) = os.path.splitext(nextFile)
			ext = ext.lower()
			autoremove = isinstance(self.files, ZipFileIterator) or isinstance(self.files, TarballFileIterator)

			if ext == '.fast5':
				nextFast5 = Fast5File(nextFile, self.group, autoremove)
			elif ext == '.tar' and tarfile.is_tarfile(nextFile) and self.oldfiles is None:
				self.set_type = FAST5SET_TARBALL
				self.oldfiles = self.files
				self.files = TarballFileIterator(nextFile, self._tmp)
				nextFast5 = self.next()
			elif ext == '.zip' and zipfile.is_zipfile(nextFile) and self.oldfiles is None:
				self.set_type = FAST5SET_ZIP
				zip = zipfile.ZipFile(nextFile, 'r', zipfile.ZIP_STORED, True)
				self.oldfiles = self.files
				self.files = ZipFileIterator( zip, self._tmp )
				nextFast5 = self.next()
			else:
				# fallthrough - hope it is a fast5!
				nextFast5 = Fast5File(nextFile, self.group, autoremove)


			return nextFast5
		except Exception as e:
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
				# Update (2/3/17) to account for new sub-directory
				# output from MinKNOW v1.4 release.
				files = [os.path.join(dirpath + os.path.sep + fast5file) \
								for dirpath, dirname, files in os.walk(f) \
									for fast5file in files]
				#pattern = f + '/' + '*.fast5'
				#files = glob.glob(pattern)
				self.files = iter(files)
				self.num_files_in_set = len(files)
				self.set_type = FAST5SET_DIRECTORY
				if not len(files):
					logger.warning("Directory is empty!")

			# is it a tarball?
			elif tarfile.is_tarfile(f):
				self.files = TarballFileIterator(f, self._tmp)
				# set to None to delay initialisation
				self.num_files_in_set = None
				self.set_type = FAST5SET_TARBALL

			# is it a zipfile?
			elif zipfile.is_zipfile(f):
				zip = zipfile.ZipFile(f, 'r', zipfile.ZIP_STORED, True)
				self.files = ZipFileIterator( zip, self._tmp )
				# set to None to delay initialisation
				self.num_files_in_set = None
				self.set_type = FAST5SET_ZIP

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

	def __init__(self, tarball, tempdir):
		self._tarball = tarball
		self._tarfile = tarfile.open(tarball)
		self._tmp = tempdir

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
		self._tarfile.extract(tarinfo, path=self._tmp)
		return os.path.join(self._tmp, tarinfo.name)

	def __len__(self):
		with tarfile.open(self._tarball) as tar:
			return len(tar.getnames())

class ZipFileIterator:
	def _fast5_filename_filter(self, filename):
		return os.path.basename(filename).endswith('.fast5') and not os.path.basename(filename).startswith('.')

	def __init__(self, zip, tempdir):
		self._zip = zip
		self._infolist = iter(zip.infolist())
		self._tmp = tempdir

	def __del__(self):
		self._zip.close()

	def __iter__(self):
		return self

	def next(self):
		zipinfo = None
		while True:
			zipinfo = next(self._infolist)
			if zipinfo and self._fast5_filename_filter( zipinfo.filename ):
				break
		if zipinfo:
			self._zip.extract(zipinfo, self._tmp)
			return os.path.join(self._tmp, zipinfo.filename )
		else:
			raise StopIteration

	def __len__(self):
		return len(self._infolist)

class Fast5File(object):

	def __init__(self, filename, group=0, autoremove=False):
		self.filename = filename
		self.group = group
		self.is_open = self.open()
		if self.is_open:
			self.version = self.guess_version()
		else:
			self.version = 'closed'

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
		if autoremove:
			os.unlink(self.filename)


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

	def guess_version(self):
		"""
		Try and guess the location of template/complement blocks
		"""
		try:
			self.hdf5file["/Analyses/Basecall_2D_%03d/BaseCalled_template" % (self.group)]
			return 'classic'
		except KeyError:
			pass

		try:
			self.hdf5file["/Analyses/Basecall_1D_%03d/BaseCalled_template" % (self.group)]
			return 'metrichor1.16'
		except KeyError:
			pass

		# less likely
                try:
                        self.hdf5file["/Analyses/Basecall_RNN_1D_%03d/BaseCalled_template" % (self.group)]
                        return 'r9rnn'
                except KeyError:
                        pass

		return 'prebasecalled'
			
	def close(self):
		"""
		Close an open an ONT Fast5 file, assuming HDF5 format
		"""
		if self.is_open:
			self.hdf5file.close()
			self.is_open = False

	def repack(self, newfile):
		"""
		Copy the contents into a new Fast5 file more optimally
		"""
		if self.is_open:
			try:
				fcopy = h5py.File(newfile, 'w')
				for x in self.hdf5file.items():
					self.hdf5file.copy(x[0], fcopy)
				fcopy.close()
			except Exception, e:
				logger.warning("Can not open a new file %s for writing!\n" % (newfile))
				return False
			return True
		else:
			return False

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
		elif choice == "best":
				fqs.append(self.fastqs.get(self.get_best_type()))

		return fqs


	def get_fastas(self, choice):
		"""
		Return the set of base called sequences in the FAST5
		in FASTQ format.
		"""
		if self.have_fastas is False:
			self._extract_fastas_from_fast5()
			self.have_fastas = True

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
		elif choice == "best":
				if self.have_fastqs is False:
					self._extract_fastqs_from_fast5()
					self.have_fastqs = True
				fas.append(self.fastas.get(self.get_best_type()))

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
			if self.keyinfo['tracking_id'].attrs['exp_start_time'].endswith('Z'):
				# MinKNOW >= 1.4 ISO format and UTC time
				dt = dateutil.parser.parse(self.keyinfo['tracking_id'].attrs['exp_start_time'])
				timestamp = int(time.mktime(dt.timetuple()))
			else:
				# Unix time stamp from MinKNOW < 1.4
				timestamp = int(self.keyinfo['tracking_id'].attrs['exp_start_time'])
			return timestamp
		except KeyError, e:
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
			return int(self.keyinfo['channel_id'].attrs['channel_number'])
		except:
			pass

		try:
			return int(self.keyinfo['read_id'].attrs['channel_number'])
		except:
			return None

	def find_read_number_block_link(self):
		"""
		Old-style FAST5/HDF5 structure:
		Inside /Analyses/Basecall_XXXX there is an 'InputEvents'
		link that points to the location of the Read in the HDF5 file.

		Return the Read's node if found, or None if not found.
		"""
		if self.version == 'classic':
			path = "/Analyses/Basecall_2D_000"
		else:
			path = "/Analyses/Basecall_1D_000"

		basecall = self.hdf5file[path]
		path = basecall.get('InputEvents', getlink=True)
		if path is None:
			return None

		# the soft link target seems broken?
		newpath = "/" + "/".join(path.path.split("/")[:-1])

		node = self.hdf5file[newpath]

		return node

	def hdf_internal_error(self,reason):
		"""Report an error and exit in case of an invalid
(or unknown) HDF5 structure. Hurrah for ONT!"""
		msg = """poretools internal error in file '%s':
%s
Please report this error (with the offending file) to:
    https://github.com/arq5x/poretools/issues""" % (self.filename, reason)
		sys.exit(msg)

        def find_read_number_block_fixed_raw(self):
		"""
		New-style FAST5/HDF5 structure:
		There is a fixed 'Raw/Reads' node with only one 'read_NNN' item
		inside it (no more 'InputEvents' link).

		Return the Read's node if found, or None if not found.
		"""
		raw_reads = self.hdf5file.get('Raw/Reads')
		if raw_reads is None:
			return None

		reads = raw_reads.keys()
		if len(reads)==0:
			self.hdf_internal_error("Raw/Reads group does not contain any items")
		if len(reads)>1:
			# This should not happen, based on information from ONT developers.
			self.hdf_internal_error("Raw/Reads group contains more than one item")
		path = 'Raw/Reads/%s' % ( reads[0] )
		node = self.hdf5file.get(path)
		if node is None:
			self.hdf_internal_error("Failed to get HDF5 item '%s'"% (path))
		return node

        def find_read_number_block(self):
		"""Returns the node of the 'Read_NNN' information, or None if not
		found"""
		node = self.find_read_number_block_link()
		if node is not None:
			return node

		node = self.find_read_number_block_fixed_raw()
		if node is not None:
			return node

		# Couldn't find the node, bail out.
		self.hdf_internal_error("unknown HDF5 structure: can't find read block item")

	def find_event_timing_block(self):
		try:
			path = fastq_paths[self.version]['template'] % (self.group)
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
				return int(node.attrs['read_number'])
			except:
				return None
		return None

	def get_start_mux(self):
		"""
		Return the mux (multiplexer) setting for this read: identify the pore with this and get_channel_number()
		"""
		node = self.find_read_number_block()
		if node:
			try:
				return int(node.attrs['start_mux'])
			except:
				return None
		return None

	def get_duration(self):
		# poretools returns in seconds not samples

		node = self.find_read_number_block_fixed_raw()
		if node:
			try:
				return int(node.attrs['duration']) / self.get_sample_frequency()
			except Exception, e:
				logger.error(str(e))
				pass

		node = self.find_event_timing_block()
		if node:
			#NOTE: 'duration' in the HDF is a float-point number,
			#      and can be less than one - which will return 0.
			#TODO: consider supporing floating-point, or at least
			#      rounding values instead of truncating to int.
			return int(node.attrs['duration'])
		return None

	def get_start_time(self):
		# poretools returns a unix timestamp not samples

		exp_start_time	= self.get_exp_start_time()

		# new raw files
		node = self.find_read_number_block_fixed_raw()
		if node:
			try:
				frequency = int(self.get_sample_frequency())
				return int(exp_start_time) + int(node.attrs['start_time'] / frequency)
			except Exception, e:
				logger.error(str(e))
				pass
 		
		node = self.find_event_timing_block()
		if node:
			return int(exp_start_time) + int(node.attrs['start_time'])
	
		return None

	def get_end_time(self):
		exp_start_time	= self.get_exp_start_time()
		start_time = self.get_start_time()
		duration = self.get_duration()

		# 'duration' can be zero and still valid
		# (if the duration of the template was less than 1 second).
		# Check for None instead of False.
		if start_time and (duration is not None):
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
			return self.keyinfo['context_tags'].attrs['version_name']
		except:
			return None

	def get_minknow_version(self):
		"""
		Return the flow cell version name.
		"""
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['context_tags'].attrs['verssion']
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
			pass

		try:
			return self.keyinfo['tracking_id'].attrs['flow_cell_id']
		except:
			return None

	def get_host_name(self):
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['hostname']
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

        def get_host_name(self):
                """
                Return the MinKNOW host computer name.
                """
                if self.have_metadata is False:
                        self._get_metadata()
                        self.have_metadata = True

                try:
                        return self.keyinfo['tracking_id'].attrs['hostname']
                except:
                        return None

                if self.have_metadata is False:
                        self._get_metadata()
                        self.have_metadata = True

	def get_device_id(self):
		"""
		Return the flowcell's device id.
		"""

                if self.have_metadata is False:
                        self._get_metadata()
                        self.have_metadata = True

		try:
			return self.keyinfo['tracking_id'].attrs['device_id']
		except:
			return None

	def get_sample_name(self):
		"""
		Return the user supplied sample name
		"""

                if self.have_metadata is False:
                        self._get_metadata()
                        self.have_metadata = True

		try:
			return self.keyinfo['context_tags'].attrs['user_filename_input']
		except Exception, e:
			return None

	def get_sample_frequency(self):
		"""
		Return the user supplied sample name
		"""

                if self.have_metadata is False:
                        self._get_metadata()
                        self.have_metadata = True

		try:
			return int(self.keyinfo['context_tags'].attrs['sample_frequency'])
		except Exception, e:
			return None

	def get_script_name(self):
		if self.have_metadata is False:
			self._get_metadata()
			self.have_metdata = True
		try:
			return self.keyinfo['tracking_id'].attrs['exp_script_name']
		except Exception, e:
			return None

	def get_template_events_count(self):
		"""
		Pull out the event count for the template strand
		"""
		try:
			table = self.hdf5file[fastq_paths[self.version]['template'] % self.group]
			return len(table['Events'][()])
		except Exception, e:
			return 0

	def get_complement_events_count(self):
		"""
		Pull out the event count for the complementary strand
		"""
		try:
			table = self.hdf5file[fastq_paths[self.version]['complement'] % self.group]
			return len(table['Events'][()])
		except Exception, e:
			return 0

	def is_high_quality(self):
		if self.get_complement_events_count() >= \
		   self.get_template_events_count():
			return True
		else:
			return False

	def get_best_type(self):
		"""
		Returns the type with the anticipated highest quality:
		'twodirections', 'template', 'complement' or None.
		"""
		try:
			if 'twodirections' in self.fastqs:
				return 'twodirections'
			fwd = 'template' in self.fastqs
			rev = 'complement' in self.fastqs
			if fwd and not rev:
				return 'template'
			elif rev and not fwd:
				return 'complement'
			else:
				fwd_err_rate = self.fastqs['template'].est_error_rate()
				rev_err_rate = self.fastqs['complement'].est_error_rate()
				if fwd_err_rate <= rev_err_rate:
					return 'template'
				else:
					return 'complement'
		except Exception, e:
			return None

	####################################################################
	# Private API methods
	####################################################################

	def _extract_fastqs_from_fast5(self):
		"""
		Return the sequence in the FAST5 file in FASTQ format
		"""
		for id, h5path in fastq_paths[self.version].iteritems(): 
			try:
				table = self.hdf5file[h5path % self.group]
				fq = formats.Fastq(table['Fastq'][()])
				fq.name += " " + self.filename
				self.fastqs[id] = fq
			except Exception, e:
				pass

	def _extract_fastas_from_fast5(self):
		"""
		Return the sequence in the FAST5 file in FASTA format
		"""
		for id, h5path in fastq_paths[self.version].iteritems(): 
			try:
				table = self.hdf5file[h5path % self.group]
				fa = formats.Fasta(table['Fastq'][()])
				fa.name += " " + self.filename
				self.fastas[id] = fa
			except Exception, e:
				pass

	def _extract_template_events(self):
		"""
		Pull out the event information for the template strand
		"""
		try:
			table = self.hdf5file[fastq_paths[self.version]['template'] % self.group]
			self.template_events = [Event(x) for x in table['Events'][()]]
		except Exception, e:
			self.template_events = []

	def _extract_complement_events(self):
		"""
		Pull out the event information for the complementary strand
		"""
		try:
			table = self.hdf5file[fastq_paths[self.version]['complement'] % self.group]
			self.complement_events = [Event(x) for x in table['Events'][()]]
		except Exception, e:
			self.complement_events = []

	def _extract_pre_basecalled_events(self):
		"""
		Pull out the pre-basecalled event information 
		"""
		# try:
		table = self.hdf5file[fastq_paths[self.version]['pre_basecalled']]
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

class Fast5ZipArchive(object):
	"""
	Creates or appends a .zip file with a directory or list of fast5 files
	"""

	def __init__(self, filename):
		"""Opens a new or appends an old zip file"""
		self.filename = args[0]
		self.zip = zipfile.ZipFile(self.filename, 'a', zipfile.ZIP_DEFLATED, True)
		self.tmp = tempfile.mkdtemp(prefix=prefix)

	def __del__(self):
		self.zip.close()
		os.rmdir(self.tmp)

	def append_dir(self, path):
		for file in os.listdir(path):
			fpath = '%s/%s' % (path,file)
			if os.path.isdir(fpath):
				self.append_dir(fpath)
			elif file.endswith('.fast5'):
				files.append_file(fpath)

	def append_file(self, filepath):
		fast5 = Fast5File(file)
		tmppath = "%s/%s" % (self.tmp, filepath)
		try:
			self.mkdirs(os.path.dirname(tmppath))
		except OSError:
			pass # okay
		fast5.repack(tmppath)
		self.zip.write(tmppath, filepath)
		os.unlink(tmppath)
		
	def append(self, *args):	
		for input in args:
			if os.path.isdir(input):
				self.append_dir(input)
			elif input.endswith('.fast5'):
				self.append_file(input)

