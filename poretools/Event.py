class Event(object):
	"""
	Very basic class to represent a nanopore 
	translocation event for a single pore
	based upon data in the Events table of 
	a Oxford Nanopore FAST5 (HDF5) file
	"""
	def __init__(self, row):
		self.row = row
		try:
			self.mean = row['mean']
		except IndexError:
			self.mean = ""
		try:
			self.start = row['start']
		except IndexError:
			self.start = ""
		try:
			self.stdv = row['stdv']
		except IndexError:
			self.stdv = ""
		try:
			self.length = row['length']
		except IndexError:
			self.length = ""
		try:
			self.model_state = row['model_state']
		except IndexError:
			self.model_state = ""
		try:
			self.model_level = row['model_level']
		except IndexError:
			self.model_level = ""
		try:
			self.move = row['move']
		except IndexError:
			self.move = ""
		try:
			self.p_model_state = row['p_model_state']
		except IndexError:
			self.p_model_state = ""
		try:
			self.mp_state = row['mp_state']
		except IndexError:
			self.mp_state = ""
		try:
			self.p_mp_state = row['p_mp_state']
		except IndexError:
			self.p_mp_state = ""
		try:
			self.p_A = row['p_A']
		except IndexError:
			self.p_A = ""
		try:
			self.p_C = row['p_C']
		except IndexError:
			self.p_C = ""
		try:
			self.p_G = row['p_G']
		except IndexError:
			self.p_G = ""
		try:
			self.p_T = row['p_T']
		except IndexError:
			self.p_T = ""

	def __repr__(self):
		return '\t'.join([str(s) for s in [self.mean, self.start, self.stdv,
										   self.length, self.model_state,
										   self.model_level, self.move,
										   self.p_model_state, 
										   self.mp_state, self.p_mp_state,
										   self.p_A, self.p_C, 
										   self.p_G, self.p_T]])
