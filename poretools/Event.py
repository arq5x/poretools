class Event(object):
	"""
	Very basic class to represent a nanopore 
	translocation event for a single pore
	based upon data in the Events table of 
	a Oxford Nanopore FAST5 (HDF5) file
	"""
	def __init__(self, row):
		self.row = row
		self.mean = row['mean']
		self.start = row['start']
		self.stdv = row['stdv']
		self.length = row['length']
		self.model_state = row['model_state']
		self.model_level = row['model_level']
		self.move = row['move']
		self.p_model_state = row['p_model_state']
		self.mp_state = row['mp_state']
		self.p_mp_state = row['p_mp_state']
		self.p_A = row['p_A']
		self.p_C = row['p_C']
		self.p_G = row['p_G']
		self.p_T = row['p_T']

	def __repr__(self):
		return '\t'.join([str(s) for s in [self.mean, self.start, self.stdv,
										   self.length, self.model_state,
										   self.model_level, self.move,
										   self.p_model_state, 
										   self.mp_state, self.p_mp_state,
										   self.p_A, self.p_C, 
										   self.p_G, self.p_T]])
