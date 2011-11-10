import urllib, urllib2
import time
import sys
import re  ## reuglar expression

try:
    from cStringIO import StringIO 
except ImportError:
    from StringIO import StringIO 

from Bio._py3k import _as_string 
#import Sequence; reload(Sequence)
from Sequence import *
import StringUtils

patternMultiSpace = re.compile("\s{2,}")
patternGoTermFull = re.compile("\[GO:\d+.*?\]")
patternGoTermExact = re.compile("(GO:\d+.*?) ")
MATCH_HREF = "<a href=\"#"
MATCH_HREF_LEN = len(MATCH_HREF)
MATCH_END_HREF = "\">"
MATCH_END_HREF_LEN = len(MATCH_END_HREF) 


sequence = "8332116"
sequence = "GO:0006468"
sequence = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALK"
sequence = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALKRKQRLRLPEWVKTDVPAGKNFARIKGNLRDLKLHTVCEEARCPNIGECWGGAEGTATATIMLMGDECTRGCRFCSIKTNKAPAPLDVDEPAHTAAAVAAWGLDYVVLTSVDRDDLPDGGSNHFASTVIELKKRKPEILVECLTPDFSGVYEDIARVAVSGLDVFAHNMETVESLTPSVRD"
sequence = "GTGTTCTACAGAGAGAAGCGTAGAGCAATAGGCTGTATTTTGAGAAAGCTGTGTGAGTGGAAAAGTGTACGGATTCTGGAAGCTGAATGCTGTGCAGATCATATCCATATGCTTGTGGAGATCCCGCCCAAAATGAGCGTATCAGGCTTTATGGGATATCTGAAAGGGAAAAGCAGTCTGATGCCTTACGAGCAGTTTGGTGATTTGAAATTCAAATACAGGAACAGGGAGTTCTGGTGCAGAGGGTATTACGTCGATACGGTGGGTAAGAACACGGCGAAGATACAGGATTACATAAAGCACCAGCTTGAAGAGGATAAAATGGGAGAGCAGTTATCGATTCCCTATCCGGGCAGCCCGTTTACGGGCCGTAAGTAA"

seq = Sequence(sequence)

## TODO refactor later
blastsAmigo(seq)
extractAccID(seq)
seq = parseGoTerm(seq) ## TODO not standard along method

seq.getAllTerms()
seq.allTerms




### functions


def blastsAmigo(seq):
    """ blast Amigo with data \
    no customise blast parameters yet"""
    parameters = [
        ('action','blast'),
        ('seq',seq.data),
        #('seq_id','FB:FBgn0015946'),
        ('CMD', 'Put')]
        
    ## query = [x for x in parameters ]
    query = parameters
    message = urllib.urlencode(query)
    
    AmigoBlastURL = "http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi"
    request = urllib2.Request(AmigoBlastURL, message, {"User-Agent":"BiopythonClient"})
    handle = urllib2.urlopen(request)
    seq.webPage = _as_string(handle.read())
    return seq

#save_file = open("testMulti.html", "w")
#save_file.write(s)  
#save_file.close()

def extractAccID(seq):
    """extract all ID and evalues"""
    key = "Sequences producing High-scoring Segment Pairs"
    endKey = "<span id="
    blastMatches = StringUtils.substring(seq.webPage, key, endKey)
    lines = blastMatches.splitlines()
    
    accID, matchID, eValue = [], [], [] ## TODO change data structure later
    ## TODO add evalue filter
    ## TODO check usage of "raise"
    #for i,l in enumerate(lines):
    for l in lines:
        if l.find(MATCH_HREF) != -1:
            token = patternMultiSpace.split(l)
            if len(token) != 4:
                raise UserWarning("Error: incorrecting parsing", token, len(token))
                print "====NEVER REACH HERE??=====", token, len(token)
                break
            start = token[0].find(MATCH_HREF)+MATCH_HREF_LEN
            mid = token[0].find(MATCH_END_HREF)
            end = token[0].find("</a>")
            accID.append(token[0][start:mid])   ## search webpage
            matchID.append(token[0][mid+MATCH_END_HREF_LEN:end])
            eValue.append(token.pop(len(token)-2)) ## or call pop() twice
    
    seq.accID = accID
    seq.matchID = matchID
    seq.eValue = eValue

    
def parseGoTerm(seq):
    """1 seq -> blast -> n hits -> m GO terms 
    ## TODO need add eValue filter
    ## TODO not standard along method"""
    resultFull, resultSummary, listGoTerm = dict(), dict(), set()    
    for m in seq.accID:
        searchKey = "<span id=\""+m+"\">"
        mIndex = seq.webPage.find(searchKey)
        endMIndex = seq.webPage.find("Length", mIndex)
        rawList = seq.webPage[mIndex:endMIndex]
        rawList = patternMultiSpace.sub(" ", rawList)
        termFullList = patternGoTermFull.findall(rawList)
        termSummaryList = patternGoTermExact.findall("".join(termFullList))
        resultFull[m] = termFullList
        resultSummary[m] = termSummaryList
        listGoTerm.update(termSummaryList)
        seq.add(m, termSummaryList)
    
    return seq
        





#### get actual GO terms
for i, eachID in enumerate(accID):

parameters2 = [
    ('gp',eachID),
    ('CMD', 'Put')]
message = urllib.urlencode(parameters2)
#http://amigo.geneontology.org/cgi-bin/amigo/gp-assoc.cgi?gp=UniProtKB:Q5BIP7&session_id=1671amigo1320698330
GOAssoc = "http://amigo.geneontology.org/cgi-bin/amigo/gp-assoc.cgi"
request = urllib2.Request(GOAssoc, message, {"User-Agent":"BiopythonClient"})

handle = urllib2.urlopen(request)
goID = _as_string(handle.read())

#save_file = open("testGetID.html", "w")
#save_file.write(goID)  
#save_file.close()



##################### others functions
#### might need add this delay thing later
# Poll NCBI until the results are ready.  Use a 3 second wait
delay = 3.0
previous = time.time()
while True:
    current = time.time()
    wait = previous + delay - current
    if wait > 0:
        #~ time.sleep(wait)
        previous = current + wait
    else:
        previous = current

    request = urllib2.Request("http://blast.ncbi.nlm.nih.gov/Blast.cgi",
                              message,
                              {"User-Agent":"BiopythonClient"})
    handle = urllib2.urlopen(request)
    results = _as_string(handle.read())
    # Can see an "\n\n" page while results are in progress,
    # if so just wait a bit longer...
    if results=="\n\n":
        continue    
    # XML results don't have the Status tag when finished
    if results.find("Status=") < 0:
        break
    i = results.index("Status=")
    j = results.index("\n", i)
    status = results[i+len("Status="):j].strip()
    if status.upper() == "READY":
        break


return StringIO(results)


















##### Functions from other places
#####

def _parse_qblast_ref_page(handle):
    """Extract a tuple of RID, RTOE from the 'please wait' page (PRIVATE).
    The NCBI FAQ pages use TOE for 'Time of Execution', so RTOE is proably
    'Request Time of Execution' and RID would be 'Request Identifier'.
    """
	s = _as_string(handle.read())
	i = s.find("RID =")
	if i == -1:
		rid = None
	else:
		j = s.find("\n", i)
		rid = s[i+len("RID ="):j].strip()

	i = s.find("RTOE =")
	if i == -1:
		rtoe = None
	else:
		j = s.find("\n", i)
		rtoe = s[i+len("RTOE ="):j].strip()

    if not rid and not rtoe:
        #Can we reliably extract the error message from the HTML page?
        #e.g.  "Message ID#24 Error: Failed to read the Blast query:
        #       Nucleotide FASTA provided for protein sequence"
        #or    "Message ID#32 Error: Query contains no data: Query
        #       contains no sequence data"
        #
        #This used to occur inside a <div class="error msInf"> entry:
        i = s.find('<div class="error msInf">')
        if i != -1:
            msg = s[i+len('<div class="error msInf">'):].strip()
            msg = msg.split("</div>",1)[0].split("\n",1)[0].strip()
            if msg:
                raise ValueError("Error message from NCBI: %s" % msg)
        #In spring 2010 the markup was like this:
        i = s.find('<p class="error">')
        if i != -1:
            msg = s[i+len('<p class="error">'):].strip()
            msg = msg.split("</p>",1)[0].split("\n",1)[0].strip()
            if msg:
                raise ValueError("Error message from NCBI: %s" % msg)
        #Generic search based on the way the error messages start:
        i = s.find('Message ID#')
        if i != -1:
            #Break the message at the first HTML tag
            msg = s[i:].split("<",1)[0].split("\n",1)[0].strip()
            raise ValueError("Error message from NCBI: %s" % msg)
        #We didn't recognise the error layout :(
        #print s
        raise ValueError("No RID and no RTOE found in the 'please wait' page, "
                         "there was probably an error in your request but we "
                         "could not extract a helpful error message.")
    elif not rid:
        #Can this happen?
        raise ValueError("No RID found in the 'please wait' page."
                           " (although RTOE = %s)" % repr(rtoe))
    elif not rtoe:
        #Can this happen?
        raise ValueError("No RTOE found in the 'please wait' page."    +                  " (although RID = %s)" % repr(rid))

    try:
        return rid, int(rtoe)
    except ValueError:
        raise ValueError("A non-integer RTOE found in "  +"the 'please wait' page, %s" % repr(rtoe))






a=10
if a>15:
    if a>20:
        print "A"
    else:
        print("B")



