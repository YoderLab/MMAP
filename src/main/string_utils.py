"""String utility class"""


def substring(s, start, end, offset=0):
    """Extract substring between "start" and "end" 
    search from position after "offset"     
    """
    
    start_index = s.find(start, offset)
    end_index = s.find(end, start_index)
    s2 = s[start_index:end_index].strip()
    return s2
    
    
