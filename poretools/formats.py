class Fastq(object):
	def __init__(self, s):
		self.s = s
		self.parse()

	def parse(self):
		(self.name, self.seq, self.sep, self.qual) = self.s.strip().split('\n')

	def __repr__(self):
		return '\n'.join([self.name, self.seq, self.sep, self.qual])

	def est_error_rate(self):
		"""
		Returns an error rate estimate using the Phred quality scores.
		"""
		try:
			error_count = 0.0
			for score in self.qual:
				phred = ord(score) - 33
				error_count += 10.0 ** (-phred / 10.0)
			return error_count / len(self.qual)
		except Exception, e:
			return 0.0



class Fasta(object):
	def __init__(self, s):
		self.s = s
		self.parse()

	def parse(self):
		(self.name, self.seq, self.sep, self.qual) = self.s.strip().split('\n')
		self.name = self.name.lstrip('@')

	def __repr__(self):
		return '\n'.join(['>'+self.name, self.seq])