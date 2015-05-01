#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $

from xml.parsers.xmlproc import xmlproc
import sys

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def split(circumstances, n):
    """Split a configuration CIRCUMSTANCES into N subsets;
       return the list of subsets"""

    subsets = []
    start = 0
    for i in range(0, n):
        len_subset = int((len(circumstances) - start) / float(n - i) + 0.5)
        subset = circumstances[start:start + len_subset]
        subsets.append(subset)
        start = start + len(subset)

    assert len(subsets) == n
    for s in subsets:
        assert len(s) > 0

    return subsets

def listminus(c1, c2):
    """Return a list of all elements of C1 that are not in C2."""
    s2 = {}
    for delta in c2:
        s2[delta] = 1
        
    c = []
    for delta in c1:
        if not s2.has_key(delta):
            c.append(delta)

    return c


def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    #assert test([]) == PASS
    #assert test(circumstances) == FAIL	
    n = 2

    while len(circumstances) >= 2:
		subsets = split(circumstances, n)
		assert len(subsets) == n

		some_complement_is_failing = 0
		for subset in subsets:
			complement = listminus(circumstances, subset)
			testStatus = test(complement)
			if testStatus == FAIL:
				circumstances = complement
				n = max(n - 1, 2)
				some_complement_is_failing = 1
				break

		if not some_complement_is_failing:
			if n == len(circumstances):
				break
			n = min(n * 2, len(circumstances))

    return circumstances


if __name__ == "__main__":
	tests = {}
	circumstances = []

	def mytest(c):
		global tests
		global circumstances
		s = ""
		for (index, string) in c:
			s += string

		out = open('input.xml', 'w')
		out.write(s)
		out.close()

		if s in tests.keys():
			return tests[s]

		print "%03i" % (len(tests.keys()) + 1), "Testing",
		try:
			app=xmlproc.Application()
			p = xmlproc.XMLProcessor()
			p.parse_resource("input.xml")
			print PASS
			tests[s] = PASS
			return PASS
		except UnboundLocalError:
			print FAIL
			tests[s] = FAIL
			return FAIL
		except:
			print UNRESOLVED
			tests[s] = UNRESOLVED
			return UNRESOLVED
	 
	if len(sys.argv) != 2:
		print "Usage: ddmin.py <filename>"
		exit(0)

	print "Delta Debugging Filname: %s " % sys.argv[1]

	index = 0
	for character in open(sys.argv[1]).read():
			circumstances.append((index, character))
			index += 1

	mytest(circumstances)
	print ddmin(circumstances, mytest)

