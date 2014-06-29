class Event(object):
	"""
	Very basic class to represent a nanopore 
	translocation event for a single pore
	based upon data in the Events table of 
	a Oxford Nanopore FAST5 (HDF5) file
	"""
	def __init__(self, row):
		self.row = row
		self.mean = row[0]
		self.start = row[1]
		self.stdv = row[2]
		self.length = row[3]
		self.model_state = row[4]
		self.model_level = row[5]
		self.move = row[6]
		self.p_model_state = row[7]
		self.mp_state = row[8]
		self.p_mp_state = row[9]
		self.p_A = row[10]
		self.p_C = row[11]
		self.p_G = row[12]
		self.p_T = row[13]
		self.raw_index = row[14]

	def __repr__(self):
		return '\t'.join([str(s) for s in self.row])