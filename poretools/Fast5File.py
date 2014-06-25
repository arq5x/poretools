import sys
import tables as pyhdf5
import formats

# TO DO:
# Create a list of paths that should be seacrhed in order of precedence (e.g. 2D v 1D)
fastq_path = '/Analyses/Basecall_2D_000/BaseCalled_template'

class Fast5File(object):

	def __init__(self, filename):
		self.filename = filename
		self.open()

		self.fasta = None
		self.fastq = None
		
		self.get_fasta()
		self.get_fastq()

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

	def get_fastq(self):
		"""
		Return the sequence in the FAST5 file in FASTQ format
		"""
		try:
			table = self.hdf5file.getNode(fastq_path)
			self.fastq = formats.Fastq(table.Fastq[()])
		except Exception, e:
			sys.stderr.write("Can't find FASTQ in %s\n" % self.filename)

	def get_fasta(self):
		"""
		Return the sequence in the FAST5 file in FASTA format
		"""
		try:
			table = self.hdf5file.getNode(fastq_path)
			self.fasta = formats.Fasta(table.Fastq[()])
		except Exception, e:
			sys.stderr.write("Can't find FASTQ in %s\n" % self.filename)
			

