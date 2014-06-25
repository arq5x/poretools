class Fastq(object):
	def __init__(self, s):
		self.s = s
		self.parse()

	def parse(self):
		(self.name, self.seq, self.sep, self.qual) = self.s.split('\n')[0:4]

	def __repr__(self):
		return '\n'.join([self.name, self.seq, self.sep, self.qual])


class Fasta(object):
	def __init__(self, s):
		self.s = s
		self.parse()

	def parse(self):
		(self.name, self.seq, self.sep, self.qual) = self.s.split('\n')[0:4]

	def __repr__(self):
		return '\n'.join(['>'+self.name, self.seq])