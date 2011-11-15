"""String utility class"""


def substring(s, start, end, after=0):
    """Extract sub string between "start" and "end" 
    search from position after "after"    
    """
    
    start_index = s.find(start, after)
    end_index = s.find(end, start_index)
    s2 = s[start_index:end_index].strip()
    return s2
    
    
