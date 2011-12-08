'''

@author: Steven Wu

connect it AmiGoS
TODO write unit test
'''


import urllib, urllib2
import time
import sys
import errno
import os
from core.utils import string_utils
from core import re_patterns
from Bio._py3k import _as_string



## check these later


### waiting time
#<h1>BLAST Query Submission</h1>

#<div class="block">
#<h2>Success!</h2>
#<p>Your job has been successfully submitted to the BLAST queue.</p>
#seq.web_page.find("Your job has been successfully submitted to the BLAST queue") 

#<a href="blast.cgi?action=get_blast_results&amp;session_id=3873amigo1320966804" title="Retrieve your BLAST job">
#"blast.cgi?action=get_blast_results&amp;session_id=3873amigo1320966804"


MATCH_HREF = "<a href=\""
MATCH_HREF_HASH = "<a href=\"#"
MATCH_HREF_HASH_LEN = len(MATCH_HREF_HASH)
MATCH_END_HREF = "\">"
MATCH_END_HREF_LEN = len(MATCH_END_HREF) 

MATCH_BLAST_WAIT = "<a href=\"blast.cgi?action=get_blast_results&amp;session_id="
MATCH_BLAST_WAIT_LEN = len(MATCH_BLAST_WAIT) 
MATCH_BLAST_END = "\" title=\"Retrieve your BLAST job\">"
MATCH_BLAST_NOT_COMPLETE = "Please be patient as your job may take several minutes to complete. "\
                            "This page will automatically refresh with the BLAST results when the job is done"

amigo_blast_URL = "http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi"

def blast_AmiGO(seq):
    """ blast Amigo with data \
    no customise blast parameters yet"""
    
    
    query_blast = [
        ('action', 'blast'),
        ('seq', seq.data),
        #('seq_id','FB:FBgn0015946'),
        ('CMD', 'Put')]
    
    seq.web_page = get_web_page(query_blast , amigo_blast_URL)
    
    delay = 3.0
    is_complete = seq.web_page.find(MATCH_BLAST_NOT_COMPLETE)
    previous = time.time()
    
    while is_complete != -1:
        current = time.time()
        wait = previous + delay - current
        if wait > 0:
            time.sleep(wait)
            print "wait %d s" % delay
            previous = current + wait
        else:
            previous = current
        session_id_index = seq.web_page.find(MATCH_BLAST_WAIT, is_complete) + MATCH_BLAST_WAIT_LEN
        session_id_index_end = seq.web_page.find(MATCH_BLAST_END, is_complete)
        session_id = seq.web_page[session_id_index:session_id_index_end]
        query_wait = [
            ('action', 'get_blast_results'),
            ('session_id', session_id),
            ('CMD', 'Put')]
        seq.web_page = get_web_page(query_wait, amigo_blast_URL)
        is_complete = seq.web_page.find(MATCH_BLAST_NOT_COMPLETE)
    
    return seq
    
    

def get_web_page(query, URL):
    
    message = urllib.urlencode(query)
    request = urllib2.Request(URL, message, {"User-Agent":"BiopythonClient"})
    handle = urllib2.urlopen(request)
    s = _as_string(handle.read())
    
    return s





def extract_ID(seq):
    """extract all ID and evalues"""
    if seq.web_page.find("*** NONE ***") == -1:
        key = "Sequences producing High-scoring Segment Pairs"
        end_key = "<span id="
        blast_matches = string_utils.substring(seq.web_page, key, end_key)
        lines = blast_matches.splitlines()

        acc_ID, match_ID, e_value = [], [], [] ## TODO change data structure later
        ## TODO add evalue filter
        ## TODO check usage of "raise"
        #for i,l in enumerate(lines):
        for l in lines:
            if l.find(MATCH_HREF_HASH) != -1:
                token = re_patterns.multi_space.split(l)
                if len(token) != 4:
                    raise UserWarning("Error: incorrecting parsing", token, len(token))
                    print "====NEVER REACH HERE??=====", token, len(token)
                    break
                start = token[0].find(MATCH_HREF_HASH) + MATCH_HREF_HASH_LEN
                mid = token[0].find(MATCH_END_HREF)
                end = token[0].find("</a>")
                acc_ID.append(token[0][start:mid])   ## search webpage
                match_ID.append(token[0][mid + MATCH_END_HREF_LEN:end])
                try:
                    v = float(token.pop(len(token) - 2) )
                    e_value.append(v) ## or call pop() twice
                except ValueError as e:
                    print 'ValueError: %s' % e;
                    print "", sys.exc_info()[0], sys.exc_info()[1]
                    raise
                   
        
        
        seq.acc_ID = acc_ID
        seq.match_ID = match_ID
        seq.e_value = e_value
        seq.is_match = True
        
    else:
        seq.is_match = False
        
    return seq
        
        

def parse_go_term(seq, e_value_cut_off=1.0):
    """1 seq -> blast -> n hits -> m GO terms 
    ## TODO need add e_value filter
    ## TODO not standard along method"""
    if seq.is_match:
        result_Full, result_Summary, list_GO_term = dict(), dict(), set()
    #    e_value_cut_off = 1e-25
        for i, m in enumerate(seq.acc_ID):
            if seq.e_value[i] < e_value_cut_off:
                search_Key = "<span id=\"" + m + "\">"
                match_index = seq.web_page.find(search_Key)
                end_match_index = seq.web_page.find("Length", match_index)
                raw_list = seq.web_page[match_index:end_match_index]
                raw_list = re_patterns.multi_space.sub(" ", raw_list)
                term_full_list = re_patterns.go_term_full.findall(raw_list)
                term_summary_list = re_patterns.go_term_exact.findall("".join(term_full_list))
                result_Full[m] = term_full_list
                result_Summary[m] = term_summary_list
                list_GO_term.update(term_summary_list)
                seq.add(m, term_summary_list)

    return seq






##### get actual GO terms
#for i, eachID in enumerate(acc_ID):

#parameters2 = [
    #('gp',eachID),
    #('CMD', 'Put')]
#message = urllib.urlencode(parameters2)
##http://amigo.geneontology.org/cgi-bin/amigo/gp-assoc.cgi?gp=UniProtKB:Q5BIP7&session_id=1671amigo1320698330
#GOAssoc = "http://amigo.geneontology.org/cgi-bin/amigo/gp-assoc.cgi"
#request = urllib2.Request(GOAssoc, message, {"User-Agent":"BiopythonClient"})

#handle = urllib2.urlopen(request)
#goID = _as_string(handle.read())

##save_file = open("testGetID.html", "w")
##save_file.write(goID)  
##save_file.close()



###################### others functions
##### might need add this delay thing later
## Poll NCBI until the results are ready.  Use a 3 second wait
#delay = 3.0
#previous = time.time()
#while True:
    #current = time.time()
    #wait = previous + delay - current
    #if wait > 0:
        ##~ time.sleep(wait)
        #previous = current + wait
    #else:
        #previous = current

    #request = urllib2.Request("http://blast.ncbi.nlm.nih.gov/Blast.cgi",
                              #message,
                              #{"User-Agent":"BiopythonClient"})
    #handle = urllib2.urlopen(request)
    #results = _as_string(handle.read())
    ## Can see an "\n\n" page while results are in progress,
    ## if so just wait a bit longer...
    #if results=="\n\n":
        #continue    
    ## XML results don't have the Status tag when finished
    #if results.find("Status=") < 0:
        #break
    #i = results.index("Status=")
    #j = results.index("\n", i)
    #status = results[i+len("Status="):j].strip()
    #if status.upper() == "READY":
        #break


#return StringIO(results)



