"""
Created on March 23, 2012

@author: Erin McKenney
"""
class GoAnalysis(object):
    """
    Calculates term frequency and % functionality of Blast.results
    """


"""
TODO: try methods for selecting GO-terms of functional interest
"""
GOterms.full = Blast.results():
z = item in GOterms.full
for item z in GOterms.full:

    # could search for a pattern within a string
    # re.search returns a match on success, None on failure
    re.search(GO, Keep, flags=0)
    # "if" loop to check whether to keep Go-term
    if "None":
        pass
    else:
        append to GOterms.functional

# try to append with +=
# assumes z is an item in list <i.e. in Keep>
# saves a LOT of time compared to if-loop
try:
    Keep += append z to GOterms.functional
except:
    pass


"""
TODO: Compare speed of methods for counting frequency
"""
# Counting frequency in a list:
GOterms = [ ]
[(a, GOterms.count(a)) for a in set(GOterms)]
sorted(_, key=lambda x:-x[1])		# add this last line to rank them

# Alternatively, you can use a Counter Class:
from collections import Counter
GOterms = " "
freqs = Counter(GOterms.split())
print(freqs)

