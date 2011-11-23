import re
"""Global class
Collection of regular pattern"""

multi_space = re.compile(r"\s{2,}")
go_term_full = re.compile(r"\[GO:\d+.*?\]")
go_term_exact = re.compile(r"(GO:\d+.*?) ")
