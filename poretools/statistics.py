def mean(l):
	"""
	Return the mean of a list of numbers
	"""
	if isinstance(l, list):
		if len(l):
			return float(sum(l)) / float(len(l))
		else:
			return None
	else:
		return None

def median(l):
	"""
	Return the median of a list of numbers
	"""
	if isinstance(l, list):
		l = sorted(l)
		if len(l) % 2 > 0:
			mid = len(l) / 2
			return l[mid]
		else:
			low = len(l) / 2 - 1
			high = len(l) / 2
			return float(l[low] + l[high]) / 2.0
	else:
		return None
