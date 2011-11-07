
import urllib, urllib2
import time
import sys
try:
    from cStringIO import StringIO ;
except ImportError:
    from StringIO import StringIO ;

from Bio._py3k import _as_string ;


# Format the "Put" command, which sends search requests to qblast.
# Parameters taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node5.html on 9 July 2007
# Additional parameters are taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node9.html on 8 Oct 2010
# To perform a PSI-BLAST or PHI-BLAST search the service ("Put" and "Get" commands) must be specified
# (e.g. psi_blast = NCBIWWW.qblast("blastp", "refseq_protein", input_sequence, service="psi"))
program = 'blastn';
database = "nt";
sequence = "8332116";



## test GO
sequence = "8332116";
sequence = "GO:0006468";
sequence = "MALVAGLSMRSGASHLVVSLAPMMAHRRFISDAAKSKLNDGPGFGEFVSGNVPLTPKALK";
#"P55269";

parameters = [
    ('action','blast'),
    ('seq',sequence),
    #('seq_id','FB:FBgn0015946'),
    ('CMD', 'Put'),
];

## query = [x for x in parameters ];
query = parameters;
message = urllib.urlencode(query);

GOBlast = "http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi";
request = urllib2.Request(GOBlast, message, {"User-Agent":"BiopythonClient"});
# http://amigo.geneontology.org/cgi-bin/amigo/blast.cgi?action=blast&seq_id=FB:FBgn0015946&session_id=9173amigo1320696173
handle = urllib2.urlopen(request);

#handle = urllib2.urlopen("http://amigo.geneontology.org/cgi-bin/amigo/term_details?term=GO:0022008")

s = _as_string(handle.read())
## save_file = open("testOut.html", "w")
## save_file.write(s)
## save_file.close()





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
        print "A";
    else:
        print("B");



