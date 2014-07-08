class Fastq(object):
	def __init__(self, s):
		self.s = s
		self.parse()

	def parse(self):
		(self.name, self.seq, self.sep, self.qual) = self.s.strip().split('\n')

	def __repr__(self):
		return '\n'.join([self.name, self.seq, self.sep, self.qual])


class Fasta(object):
	def __init__(self, s):
		self.s = s
		self.parse()

	def parse(self):
		(self.name, self.seq, self.sep, self.qual) = self.s.strip().split('\n')
		self.name = self.name.lstrip('@')

	def __repr__(self):
		return '\n'.join(['>'+self.name, self.seq])