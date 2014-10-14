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

def NX(l, x=[25,50,75]):
        """
        Returns NX for all x for a list of numbers l.
        Default: N25, N50, N75
        Assumes all values in list x are between 0 and 100.
        Interpretation: When NX = NX_value, X% of data (in bp) is contained in reads at least NX_value bp long.
        """
	if isinstance(l, list) and isinstance(x, list):
		l = sorted(l)
		x = sorted(x)
		total = sum(l)
                nxsum = 0
                nxvalues = {e:0 for e in x}
		for e in x:
                        xpct = total*e/100.0
                        while nxsum < xpct and l:
                                nxsum += l[-1]
                                lastsize = l.pop()
                        nxvalues[e] = lastsize
                return nxvalues

	else:
		return None
