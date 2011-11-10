def substring(s, start, end):
    """Extract sub string between "start" and "end" """
    startIndex = s.index(start)
    endIndex   = s.index(end, startIndex)
    s2 = s[startIndex:endIndex].strip()
    return s2
    
    