import re
"""Collection of regular pattern"""

multi_space = re.compile("\s{2,}")
go_term_full = re.compile("\[GO:\d+.*?\]")
go_term_exact = re.compile("(GO:\d+.*?) ")
