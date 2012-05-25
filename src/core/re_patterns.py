'''

@author: Steven Wu
'''


import re
"""Global class
Collection of regular pattern"""

multi_space = re.compile(r"\s{2,}")
go_term_full = re.compile(r"\[GO:\d+.*?\]")
go_term_exact = re.compile(r"(GO:\d+.*?) ")


def multi_space_sub(pat, s):
    return multi_space.sub(pat, s)


def multi_space_split(s):
    return multi_space.split(s)


def go_term_full_findall(s):
    return go_term_full.findall(s)


def go_term_exact_findall(s):
    return go_term_exact.findall(s)
